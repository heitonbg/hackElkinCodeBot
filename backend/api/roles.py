"""
Быстрый API для ролей и сценариев — без AI, мгновенные ответы.
"""
import json
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.role_matcher import match_roles, get_all_roles, search_roles, get_role_scenario
from services.scenario_scorer import score_scenario, score_scenario_with_feedback
from services.async_analyzer import analyze_scenario_results
from services.achievement_service import check_test_achievements
from database.db import db

logger = logging.getLogger(__name__)
router = APIRouter()

class RoleMatchRequest(BaseModel):
    telegram_id: str

class ScenarioScoreRequest(BaseModel):
    telegram_id: str
    role_id: str
    level: str = "junior"
    answers: List[dict]  # [{"question_id": "...", "answer": "..."}]


@router.post("/match")
async def match_roles_api(data: RoleMatchRequest):
    """Rule-based матчинг ролей — мгновенно"""
    user = await db.get_user(data.telegram_id)
    if not user:
        return {"roles": [], "error": "Пользователь не найден. Пройдите онбординг."}

    user_data = {
        "education": user.get("education", ""),
        "field": user.get("field", ""),
        "experience": user.get("experience", ""),
        "interests": json.loads(user["interests"]) if user["interests"] else [],
        "skills": json.loads(user["skills"]) if user["skills"] else [],
        "career_goals": json.loads(user["career_goals"]) if user["career_goals"] else [],
    }

    roles = match_roles(user_data)
    return {"roles": roles, "count": len(roles)}


@router.get("/all")
async def get_all_roles_api():
    """Все роли (для поиска)"""
    roles = get_all_roles()
    # Упрощённый формат
    simplified = [
        {
            "role_id": r["role_id"],
            "title": r["title"],
            "category": r["category"],
            "scenarios_available": list(r.get("scenarios", {}).keys()),
        }
        for r in roles
    ]
    return {"roles": simplified, "count": len(simplified)}


@router.get("/search")
async def search_roles_api(q: str = ""):
    """Поиск ролей по названию"""
    results = search_roles(q)
    return {"roles": results, "count": len(results)}


@router.get("/scenario/{role_id}")
async def get_scenario_api(role_id: str, level: str = "junior"):
    """Получить сценарий для роли"""
    scenario = get_role_scenario(role_id, level)
    if not scenario:
        return {"error": "Сценарий не найден"}
    return scenario


@router.post("/score")
async def score_scenario_api(data: ScenarioScoreRequest):
    """
    Скоринг сценария — мгновенно, rule-based.
    + запуск фонового AI-анализа.
    """
    # Получаем сценарий
    scenario = get_role_scenario(data.role_id, data.level)
    if not scenario:
        return {"error": "Сценарий не найден"}

    questions = scenario.get("questions", [])
    result = score_scenario_with_feedback(questions, data.answers)

    # Сохраняем rule-based результат в БД
    try:
        await db.save_scenario_result(data.telegram_id, data.role_id, {
            "match_score": result["match_score"],
            "level": data.level,
            "level_label": result["level_label"],
            "details": result.get("details", []),
        })
    except Exception as e:
        logger.warning(f"Не удалось сохранить результат: {e}")

    # Запускаем фоновый AI-анализ (не блокируем ответ)
    user = await db.get_user(data.telegram_id)
    if user:
        user_profile = {
            "education": user.get("education", ""),
            "field": user.get("field", ""),
            "experience": user.get("experience", ""),
            "skills": json.loads(user["skills"]) if user["skills"] else [],
        }
        # Фоновая задача — не ждём
        import asyncio
        asyncio.create_task(
            analyze_scenario_results(data.telegram_id, data.role_id, result, user_profile)
        )

    # Проверяем достижения
    stats = await db.get_user_scenario_stats(data.telegram_id)
    total_tests = len(stats)
    unique_roles = len(set(s["role_id"] for s in stats))
    avg_score = sum(s["match_score"] for s in stats) / max(1, len(stats))

    new_achievements = await check_test_achievements(
        telegram_id=data.telegram_id,
        role_id=data.role_id,
        score=result["match_score"],
        total_tests=total_tests,
        unique_roles=unique_roles,
        avg_score=avg_score,
    )

    return {
        "role_id": data.role_id,
        "title": scenario.get("title", ""),
        "level": data.level,
        "new_achievements": new_achievements,
        **result,
    }


@router.get("/ai-analysis/{telegram_id}")
async def get_ai_analysis_api(telegram_id: str, role_id: str = None):
    """Получить AI-анализ (если готов)"""
    if role_id:
        analysis = await db.get_ai_analysis(telegram_id, role_id)
        return {"analysis": analysis} if analysis else {"analysis": None, "status": "pending"}
    else:
        analyses = await db.get_ai_analysis(telegram_id)
        return {"analyses": analyses or []}

"""
API роутер для Daily Challenges.
"""
import json
import logging
from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from database.db import db
from services.daily_challenge_service import generate_daily_challenge, evaluate_daily_answer
from services.achievement_service import check_daily_achievements, check_diagnostic_achievement
from services.role_matcher import get_all_roles

logger = logging.getLogger(__name__)
router = APIRouter()


class DailyAnswerRequest(BaseModel):
    telegram_id: str
    answer: str


@router.get("/challenge")
async def get_daily_challenge(telegram_id: str, role_id: str = None):
    """
    Получить ситуацию на сегодня.
    Если role_id не указан — берём лучшую роль пользователя.
    """
    today = datetime.now().date().isoformat()

    # Пробуем найти существующую ситуацию
    existing = await db.get_daily_challenge(telegram_id, today)
    if existing:
        return existing

    # Определяем роль
    if not role_id:
        # Берём лучшую роль по результатам тестов
        stats = await db.get_user_scenario_stats(telegram_id)
        if stats:
            best = max(stats, key=lambda x: x.get("match_score", 0))
            role_id = best.get("role_id")

    if not role_id:
        # Fallback — первая роль из БД
        all_roles = get_all_roles()
        if all_roles:
            role_id = all_roles[0]["role_id"]
        else:
            return {"error": "Нет доступных ролей"}

    # Находим название роли
    role_title = role_id.replace("_", " ").title()
    all_roles = get_all_roles()
    for r in all_roles:
        if r["role_id"] == role_id:
            role_title = r["title"]
            break

    # Генерируем ситуацию
    challenge = await generate_daily_challenge(role_id, role_title)

    # Сохраняем
    await db.save_daily_challenge(telegram_id, role_id, challenge["situation"], today)

    # Возвращаем
    return {
        "id": None,  # Will be set after save
        "role_id": role_id,
        "role_title": role_title,
        "situation_text": challenge["situation"],
        "ideal_keywords": challenge["ideal_keywords"],
        "challenge_date": today,
        "answered": False,
    }


@router.post("/answer")
async def submit_daily_answer(data: DailyAnswerRequest):
    """Отправить ответ на ситуацию"""
    today = datetime.now().date().isoformat()

    # Находим ситуацию
    challenge = await db.get_daily_challenge(data.telegram_id, today)
    if not challenge:
        return {"error": "Нет ситуации на сегодня. Сначала получите challenge."}

    if challenge["answered"]:
        return {"error": "Вы уже ответили сегодня!", "ai_score": challenge["ai_score"], "ai_feedback": challenge["ai_feedback"]}

    # Получаем идеальные ключевые слова
    all_roles = get_all_roles()
    role_title = challenge["role_id"].replace("_", " ").title()
    for r in all_roles:
        if r["role_id"] == challenge["role_id"]:
            role_title = r["title"]
            break

    # Для идеальных keywords — генерируем на лету (т.к. не сохраняем)
    # Используем простой fallback
    ideal_keywords = ["профессиональный подход", "конкретика", "практическое решение"]

    # Оцениваем ответ
    result = await evaluate_daily_answer(
        role_title=role_title,
        situation=challenge["situation_text"],
        ideal_keywords=ideal_keywords,
        user_answer=data.answer,
    )

    # Сохраняем
    await db.submit_daily_answer(challenge["id"], data.answer, result["score"], result["feedback"])

    # Получаем streak
    streak_data = await db.get_daily_streak(data.telegram_id)

    # Проверяем достижения
    new_achievements = await check_daily_achievements(
        telegram_id=data.telegram_id,
        score=result["score"],
        streak=streak_data["streak"],
        best_streak=streak_data["best_streak"],
        total_daily=streak_data["total_completed"],
    )

    return {
        "ai_score": result["score"],
        "ai_feedback": result["feedback"],
        "streak": streak_data["streak"],
        "best_streak": streak_data["best_streak"],
        "new_achievements": new_achievements,
    }


@router.get("/streak")
async def get_streak(telegram_id: str):
    """Получить streak и статистику"""
    streak_data = await db.get_daily_streak(telegram_id)
    history = await db.get_daily_history(telegram_id, limit=5)

    return {
        **streak_data,
        "recent": history,
    }

"""
API для онбординга и диагностики.
"""
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from services.diagnostic_scorer import (
    get_diagnostic_questions,
    score_diagnostic,
    save_diagnostic_result,
)
from services.role_matcher import get_all_roles, search_roles
from services.achievement_service import check_diagnostic_achievement
from database.db import db

logger = logging.getLogger(__name__)
router = APIRouter()


class DiagnosticAnswer(BaseModel):
    question_id: str
    answer: str


class DiagnosticRequest(BaseModel):
    telegram_id: str
    answers: List[DiagnosticAnswer]


class SaveProfileRequest(BaseModel):
    telegram_id: str
    education: Optional[str] = ""
    field: Optional[str] = ""
    experience: Optional[str] = ""
    interests: List[str] = []
    skills: List[str] = []
    career_goals: List[str] = []


@router.get("/questions")
async def get_questions():
    """Получить все диагностические вопросы"""
    questions = get_diagnostic_questions()
    return {"questions": questions, "count": len(questions)}


@router.post("/diagnostic")
async def run_diagnostic(data: DiagnosticRequest):
    """
    Пройти диагностику и получить рекомендации ролей.
    
    Сохраняет профиль пользователя и возвращает:
    - top_categories: топ категорий по баллам
    - recommended_roles: рекомендованные роли
    """
    # Преобразуем ответы в формат dict
    answers = [{"question_id": a.question_id, "answer": a.answer} for a in data.answers]
    
    # Скоринг
    results = score_diagnostic(answers)
    
    # Сохраняем профиль (обновляем поле field на основе топ категории)
    if results["top_categories"]:
        top_category = results["top_categories"][0]
        await db.save_user(data.telegram_id, {
            "education": "",
            "field": top_category["category_name"],
            "experience": "",
            "interests": [],
            "skills": [],
            "career_goals": [],
        })
    
    # Сохраняем результаты диагностики
    save_diagnostic_result(data.telegram_id, answers, results)

    # Проверяем достижение
    new_achievements = await check_diagnostic_achievement(data.telegram_id)

    return {**results, "new_achievements": new_achievements}


@router.post("/save-profile")
async def save_profile(data: SaveProfileRequest):
    """Сохранить профиль пользователя после диагностики"""
    await db.save_user(data.telegram_id, {
        "education": data.education,
        "field": data.field,
        "experience": data.experience,
        "interests": data.interests,
        "skills": data.skills,
        "career_goals": data.career_goals,
    })
    return {"status": "success", "message": "Профиль сохранён"}


@router.get("/roles/all")
async def get_all_roles_api():
    """Все роли (для поиска)"""
    roles = get_all_roles()
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


@router.get("/roles/search")
async def search_roles_api(q: str = ""):
    """Поиск ролей по названию"""
    results = search_roles(q)
    return {"roles": results, "count": len(results)}

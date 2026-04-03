from fastapi import APIRouter
import json
import logging
from models.models import CareerAnalysis
from database.db import db
from services.ai_service import analyze_career

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze")
async def analyze_career_path(data: CareerAnalysis):
    """AI анализ карьерного пути пользователя"""
    logger.info(f"Запрос анализа карьеры для пользователя {data.telegram_id}")
    user = await db.get_user(data.telegram_id)
    if not user:
        logger.warning(f"Пользователь {data.telegram_id} не найден в БД")
        return {"error": "Пользователь не найден. Пройдите онбординг."}

    user_data = {
        "education": user.get("education", "не указано"),
        "field": user.get("field", "не указано"),
        "experience": user.get("experience", "не указан"),
        "interests": json.loads(user["interests"]) if user["interests"] else [],
        "skills": json.loads(user["skills"]) if user["skills"] else [],
        "career_goals": json.loads(user["career_goals"]) if user["career_goals"] else [],
    }

    logger.info(f"Данные пользователя: {user_data['education']}, {user_data['field']}, {len(user_data['skills'])} навыков")
    analysis = await analyze_career(user_data)
    await db.save_analysis(data.telegram_id, analysis)

    logger.info(f"Анализ сохранен для {data.telegram_id}")
    return {"status": "success", "analysis": analysis}

@router.get("/result/{telegram_id}")
async def get_analysis_result(telegram_id: str):
    """Получение последнего анализа"""
    user = await db.get_user(telegram_id)
    if not user:
        return {"error": "Пользователь не найден"}

    # Получаем анализ из БД
    analysis = await db.get_latest_analysis(telegram_id)
    
    if not analysis:
        return {
            "professions": [],
            "career_path": [],
            "missing_skills": [],
            "message": "Пройдите анализ для получения результатов"
        }

    return analysis

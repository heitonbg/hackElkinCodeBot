from fastapi import APIRouter
import json
from models.models import OnboardingData
from database.db import db

router = APIRouter()

@router.post("/onboarding")
async def save_onboarding(data: OnboardingData):
    """Сохранение данных онбординга пользователя (не трогает Telegram поля)"""
    await db.save_onboarding_data(data.telegram_id, {
        "education": data.education,
        "field": data.field,
        "experience": data.experience,
        "interests": data.interests,
        "skills": data.skills,
        "career_goals": data.career_goals,
    })
    return {"status": "success", "message": "Данные сохранены"}

@router.get("/profile/{telegram_id}")
async def get_profile(telegram_id: str):
    """Получение профиля пользователя"""
    user = await db.get_user(telegram_id)
    if not user:
        return {"exists": False, "profile": None}

    user["interests"] = json.loads(user["interests"]) if user["interests"] else []
    user["skills"] = json.loads(user["skills"]) if user["skills"] else []
    user["career_goals"] = json.loads(user["career_goals"]) if user["career_goals"] else []

    # Добавляем Telegram-данные в ответ
    telegram_data = {
        "telegram_username": user.get("username"),
        "telegram_first_name": user.get("first_name"),
        "telegram_last_name": user.get("last_name"),
        "telegram_photo_url": user.get("photo_url"),
        "telegram_language_code": user.get("language_code"),
    }

    return {
        "exists": True, 
        "profile": user,
        "telegram": telegram_data,
    }

@router.get("/stats/{telegram_id}")
async def get_user_stats(telegram_id: str):
    """Статистика пользователя для дашборда"""
    user = await db.get_user(telegram_id)
    if not user:
        return {"exists": False}

    skills = json.loads(user["skills"]) if user["skills"] else []
    interests = json.loads(user["interests"]) if user["interests"] else []
    career_goals = json.loads(user["career_goals"]) if user["career_goals"] else []

    analysis = await db.get_latest_analysis(telegram_id)
    has_analysis = analysis is not None

    total_fields = 5
    filled_fields = sum([
        1 if user.get("education") else 0,
        1 if user.get("field") else 0,
        1 if user.get("experience") else 0,
        1 if len(interests) > 0 else 0,
        1 if len(skills) > 0 else 0,
    ])
    profile_complete = round(filled_fields / total_fields * 100)

    return {
        "exists": True,
        "skills_count": len(skills),
        "interests_count": len(interests),
        "goals_count": len(career_goals),
        "has_analysis": has_analysis,
        "profile_complete": profile_complete
    }

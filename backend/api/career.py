from fastapi import APIRouter
import json
import logging
from models.models import CareerAnalysis, RoleGenerationRequest, ScenarioGenerationRequest
from database.db import db
from services.ai_service import analyze_career, get_skill_recommendations, generate_roles_for_profile, generate_scenario_for_role

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

@router.post("/quick-match")
async def quick_match(data: CareerAnalysis):
    """Быстрый AI матчинг — только профессии с % совпадения"""
    user = await db.get_user(data.telegram_id)
    if not user:
        return {"professions": []}

    from services.ai_service import quick_match_career

    user_data = {
        "education": user.get("education", ""),
        "field": user.get("field", ""),
        "experience": user.get("experience", ""),
        "interests": json.loads(user["interests"]) if user["interests"] else [],
        "skills": json.loads(user["skills"]) if user["skills"] else [],
        "career_goals": json.loads(user["career_goals"]) if user["career_goals"] else [],
    }

    result = await quick_match_career(user_data)
    return result

@router.get("/recommendations/{telegram_id}")
async def get_recommendations(telegram_id: str):
    """Персональные рекомендации по развитию навыков"""
    try:
        user = await db.get_user(telegram_id)
        if not user:
            return {"error": "Пользователь не найден. Пройдите онбординг."}

        user_data = {
            "education": user.get("education", ""),
            "field": user.get("field", ""),
            "profession": user.get("field", ""),
            "experience": user.get("experience", ""),
            "interests": json.loads(user["interests"]) if user.get("interests") else [],
            "skills": json.loads(user["skills"]) if user.get("skills") else [],
            "career_goals": json.loads(user["career_goals"]) if user.get("career_goals") else [],
        }

        # Получаем результаты тестирования
        try:
            test_results = await db.get_user_scenario_stats(telegram_id)
            test_results_list = []
            if test_results:
                test_results_list = [{"role_id": r.get("role_id", ""), "match_score": r.get("match_score", 0)} for r in test_results]
        except:
            test_results_list = []

        recommendations = await get_skill_recommendations(user_data, test_results_list)
        return recommendations
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Recommendations error: {e}", exc_info=True)
        # Возвращаем моковые рекомендации
        from services.ai_service import _get_mock_recommendations
        return _get_mock_recommendations({"field": "специалист", "skills": []})

@router.post("/generate-roles")
async def generate_roles(data: RoleGenerationRequest):
    """AI генерация динамического списка ролей на основе профиля"""
    logger.info(f"Запрос AI-генерации ролей для пользователя {data.telegram_id}")
    user = await db.get_user(data.telegram_id)
    if not user:
        logger.warning(f"Пользователь {data.telegram_id} не найден в БД")
        return {"error": "Пользователь не найден. Пройдите онбординг."}

    user_data = {
        "education": user.get("education", "не указано"),
        "field": user.get("field", "не указано"),
        "profession": user.get("field", "не указано"),
        "experience": user.get("experience", "не указан"),
        "interests": json.loads(user["interests"]) if user["interests"] else [],
        "skills": json.loads(user["skills"]) if user["skills"] else [],
        "career_goals": json.loads(user["career_goals"]) if user["career_goals"] else [],
    }

    logger.info(f"AI генерация ролей: профиль — {user_data['field']}, {len(user_data['skills'])} навыков")
    result = await generate_roles_for_profile(user_data)
    return result

@router.post("/generate-scenario")
async def generate_scenario(data: ScenarioGenerationRequest):
    """AI генерация сценария для конкретной роли"""
    logger.info(f"Запрос AI-генерации сценария: {data.role_id} для пользователя {data.telegram_id}")
    user = await db.get_user(data.telegram_id)
    if not user:
        logger.warning(f"Пользователь {data.telegram_id} не найден в БД")
        return {"error": "Пользователь не найден."}

    # Проверяем, есть ли уже сгенерированный сценарий
    cached = await db.get_generated_scenario(data.telegram_id, data.role_id)
    if cached:
        logger.info(f"Найден кэшированный сценарий для {data.role_id}")
        # Удаляем created_at из кэша
        cached.pop("created_at", None)
        return cached

    user_data = {
        "education": user.get("education", "не указано"),
        "experience": user.get("experience", "не указан"),
        "skills": json.loads(user["skills"]) if user["skills"] else [],
    }

    role_data = data.role_data or {}
    logger.info(f"AI генерация сценария: {role_data.get('title', data.role_id)}")
    scenario = await generate_scenario_for_role(role_data, user_data)

    # Сохраняем в кэш
    try:
        await db.save_generated_scenario(data.telegram_id, data.role_id, scenario)
    except Exception as e:
        logger.warning(f"Не удалось сохранить сценарий: {e}")

    return scenario

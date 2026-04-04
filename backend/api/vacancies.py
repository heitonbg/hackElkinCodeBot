from fastapi import APIRouter
import json
from models.models import VacancyFilter
from services.hh_service import search_vacancies
from services.matching_service import match_vacancies
from database.db import db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/search")
async def search_vacancies_api(profession: str = "", location: str = "", limit: int = 20):
    """Поиск вакансий на HH.ru"""
    try:
        logger.info(f"Поиск вакансий: profession='{profession}', location='{location}', limit={limit}")
        vacancies = await search_vacancies(profession, location, limit)
        logger.info(f"Найдено {len(vacancies)} вакансий")
        return {"vacancies": vacancies, "count": len(vacancies), "source": "hh.ru"}
    except Exception as e:
        logger.error(f"HH search error: {e}", exc_info=True)
        return {
            "vacancies": [],
            "count": 0,
            "error": f"Не удалось подключиться к HH.ru: {str(e)}",
            "source": "error"
        }

@router.post("/match")
async def match_vacancies_api(data: VacancyFilter):
    """Матчинг вакансий под профиль пользователя"""
    user = await db.get_user(data.telegram_id)
    if not user:
        return {"error": "Пользователь не найден"}

    user_skills = json.loads(user["skills"]) if user["skills"] else []

    # Получаем вакансии
    vacancies = await search_vacancies(data.profession, data.location)

    # Матчинг
    matched = await match_vacancies(user_skills, vacancies)

    return {"matched_vacancies": matched, "count": len(matched)}

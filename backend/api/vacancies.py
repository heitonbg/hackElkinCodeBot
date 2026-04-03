from fastapi import APIRouter
import json
from models.models import VacancyFilter
from services.hh_service import search_vacancies
from services.matching_service import match_vacancies
from services.mts_vacancies import get_all_mts_vacancies, get_it_vacancies
from services.mts_matching import match_user_to_mts_vacancies, get_top_matches
from database.db import db

router = APIRouter()

@router.get("/search")
async def search_vacancies_api(profession: str = "", location: str = "", limit: int = 20):
    """Поиск вакансий на HH.ru"""
    vacancies = await search_vacancies(profession, location, limit)
    return {"vacancies": vacancies, "count": len(vacancies)}

@router.get("/mts")
async def get_mts_vacancies_api(only_it: bool = True):
    """Получение вакансий МТС из матрицы компетенций"""
    vacancies = get_it_vacancies() if only_it else get_all_mts_vacancies()
    return {"vacancies": vacancies, "count": len(vacancies)}

@router.get("/mts/match/{telegram_id}")
async def match_mts_vacancies_api(telegram_id: str, top_n: int = 10):
    """Матчинг пользователя с вакансиями МТС"""
    user = await db.get_user(telegram_id)
    if not user:
        return {"error": "Пользователь не найден. Пройдите онбординг."}

    user_skills = json.loads(user["skills"]) if user["skills"] else []
    user_interests = json.loads(user["interests"]) if user["interests"] else []

    matched = get_top_matches(user_skills, user_interests, top_n)
    return {"matched_vacancies": matched, "count": len(matched)}

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

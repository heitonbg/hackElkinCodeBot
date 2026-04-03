import os
import httpx
from dotenv import load_dotenv

# Загружаем .env из корня проекта
_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

HH_USER_AGENT = "HH-User-Agent"
HH_API_URL = "https://api.hh.ru"


async def search_vacancies(profession: str = "", location: str = "", limit: int = 20) -> list:
    """Поиск вакансий на HH.ru"""
    params = {
        "text": profession or "IT программист",
        "per_page": limit,
        "area": "113",  # Россия
    }

    if location:
        params["area"] = location

    headers = {"User-Agent": HH_USER_AGENT}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{HH_API_URL}/vacancies", params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

            vacancies = []
            for item in data.get("items", []):
                vacancies.append({
                    "id": item.get("id"),
                    "title": item.get("name", "Без названия"),
                    "company": item.get("employer", {}).get("name", "Не указана"),
                    "salary": _format_salary(item.get("salary")),
                    "url": item.get("alternate_url", ""),
                    "location": item.get("area", {}).get("name", "") if item.get("area") else "",
                    "description_snippet": item.get("snippet", {}).get("requirement", ""),
                    "published": item.get("published_at", ""),
                })

            return vacancies
    except Exception as e:
        print(f"HH API Error: {e}")
        return _get_mock_vacancies(profession)


async def get_vacancy_details(vacancy_id: str) -> dict:
    """Детальная информация о вакансии"""
    headers = {"User-Agent": HH_USER_AGENT}
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{HH_API_URL}/vacancies/{vacancy_id}", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            return {
                "id": data.get("id"),
                "title": data.get("name", ""),
                "company": data.get("employer", {}).get("name", ""),
                "salary": _format_salary(data.get("salary")),
                "description": data.get("description", ""),
                "requirements": _extract_requirements(data),
                "url": data.get("alternate_url", ""),
                "location": data.get("area", {}).get("name", "") if data.get("area") else "",
            }
    except Exception as e:
        print(f"HH API Error: {e}")
        return {}


def _format_salary(salary: dict) -> str:
    """Форматирование зарплаты"""
    if not salary:
        return "По договорённости"
    
    salary_str = ""
    if salary.get("from"):
        salary_str += f"от {salary['from']:,}"
    if salary.get("to"):
        salary_str += f" до {salary['to']:,}"
    
    currency = salary.get("currency", "RUR")
    currency_symbol = {"RUR": "₽", "USD": "$", "EUR": "€"}.get(currency, currency)
    
    return f"{salary_str} {currency_symbol}".strip() if salary_str else "По договорённости"


def _extract_requirements(vacancy_data: dict) -> list:
    """Извлечение требований из описания"""
    description = vacancy_data.get("description", "")
    # Упрощённая логика — можно улучшить с AI
    key_skills = vacancy_data.get("key_skills", [])
    return [skill.get("name", "") for skill in key_skills] if key_skills else []


def _get_mock_vacancies(profession: str) -> list:
    """Mock вакансии для тестов"""
    return [
        {
            "id": "1",
            "title": f"Junior {profession or 'Data Analyst'}",
            "company": "МТС Digital",
            "salary": "от 60,000 ₽",
            "url": "https://hh.ru",
            "location": "Москва",
            "description_snippet": "Ищем аналитика данных с опытом работы с Python и SQL",
            "published": "2024-01-01",
        },
        {
            "id": "2",
            "title": f"Middle {profession or 'Data Analyst'}",
            "company": "СберТех",
            "salary": "от 120,000 ₽",
            "url": "https://hh.ru",
            "location": "Москва (удалённо)",
            "description_snippet": "Требуется опыт с Pandas, NumPy, визуализацией данных",
            "published": "2024-01-02",
        },
        {
            "id": "3",
            "title": f"Senior {profession or 'Python Developer'}",
            "company": "Яндекс",
            "salary": "от 200,000 ₽",
            "url": "https://hh.ru",
            "location": "Удалённо",
            "description_snippet": "Разработка высоконагруженных сервисов на Python",
            "published": "2024-01-03",
        },
        {
            "id": "4",
            "title": f"Product Manager",
            "company": "Тинькофф",
            "salary": "от 150,000 ₽",
            "url": "https://hh.ru",
            "location": "Москва",
            "description_snippet": "Управление продуктом, работа с метриками",
            "published": "2024-01-04",
        },
        {
            "id": "5",
            "title": f"Junior Frontend Developer",
            "company": "VK",
            "salary": "от 80,000 ₽",
            "url": "https://hh.ru",
            "location": "Санкт-Петербург",
            "description_snippet": "React, TypeScript, работа в команде",
            "published": "2024-01-05",
        },
    ]

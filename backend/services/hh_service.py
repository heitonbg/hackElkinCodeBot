import os
import re
import asyncio
import time
import httpx
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Загружаем .env из корня проекта
_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

HH_USER_AGENT = os.getenv("HH_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
HH_API_URL = "https://api.hh.ru"

# Кешированный справочник городов
_areas_cache = None
_areas_cache_time = 0

# Кэш результатов поиска HH.ru (5 минут)
_hh_search_cache = {}
HH_CACHE_TTL = 300  # 5 минут

# Маппинг популярных городов (проверенные area_id)
AREA_MAP = {
    "москва": "1",
    "московская область": "1",
    "санкт-петербург": "2",
    "питер": "2",
    "spb": "2",
    "казань": "113",  # Вся Россия, Казань нет отдельного ID
    "новосибирск": "4",
    "екатеринбург": "3",
    "нижний новгород": "55",
    "самара": "59",
    "краснодар": "48",
    "ростов-на-дону": "60",
    "уфа": "64",
    "челябинск": "65",
    "волгоград": "58",
    "пермь": "63",
    "красноярск": "53",
    "воронеж": "51",
    "томск": "68",
    "тюмень": "71",
    "иркутск": "52",
    "хабаровск": "74",
    "владивосток": "56",
    "омск": "62",
    "сочи": "66",
    "калининград": "54",
    "ярославль": "76",
}


async def _find_area_id(city_name: str) -> str:
    """Найти area_id города через справочник HH"""
    mapped = AREA_MAP.get(city_name.lower())
    if mapped:
        return mapped

    global _areas_cache, _areas_cache_time
    import time
    headers = {"User-Agent": HH_USER_AGENT}

    # Кеш на 1 час
    if _areas_cache and (time.time() - _areas_cache_time) < 3600:
        return _search_area_recursive(_areas_cache, city_name.lower())

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{HH_API_URL}/areas", headers=headers)
            if resp.status_code == 200:
                areas = resp.json()
                _areas_cache = areas
                _areas_cache_time = time.time()
                return _search_area_recursive(areas, city_name.lower())
    except Exception as e:
        print(f"Не удалось загрузить справочник городов: {e}")
    return "113"


def _search_area_recursive(areas, query):
    for area in areas:
        name = area.get("name", "").lower()
        if query in name or name in query:
            return str(area["id"])
        sub = area.get("areas", [])
        if sub:
            result = _search_area_recursive(sub, query)
            if result:
                return result
        cities = area.get("cities", [])
        for city in cities:
            if query in city.get("name", "").lower():
                return str(city["id"])
    return "113"


async def search_vacancies(profession: str = "", location: str = "", limit: int = 20) -> list:
    """Поиск вакансий на HH.ru — с кэшированием"""
    cache_key = f"{profession}:{location}:{limit}"
    if cache_key in _hh_search_cache:
        cached = _hh_search_cache[cache_key]
        if time.time() - cached["time"] < HH_CACHE_TTL:
            logger.info(f"HH cache hit: {cache_key}")
            return cached["data"]
        else:
            del _hh_search_cache[cache_key]

    params = {
        "text": profession or "стажер",
        "per_page": min(limit, 20),
    }

    if location and location.strip():
        loc_lower = location.strip().lower()
        if loc_lower in AREA_MAP:
            mapped = AREA_MAP[loc_lower]
            if mapped != "113":
                params["area"] = mapped
            else:
                params["text"] = f"{params['text']} {location.strip()}"
        else:
            area_id = await _find_area_id(location.strip())
            if area_id and area_id != "113":
                params["area"] = area_id
            else:
                params["text"] = f"{params['text']} {location.strip()}"

    headers = {"User-Agent": HH_USER_AGENT}

    async with httpx.AsyncClient(timeout=10) as client:
        for attempt in range(3):
            response = await client.get(f"{HH_API_URL}/vacancies", params=params, headers=headers)
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 2 ** attempt))
                logger.warning(f"HH rate limit, ждём {retry_after}с...")
                await asyncio.sleep(retry_after)
                continue
            response.raise_for_status()
            break
        else:
            raise Exception("HH.ru rate limit exceeded")

        data = response.json()
        items = data.get("items", [])[:limit]

        detail_ids = [item.get("id") for item in items[:3] if item.get("id")]
        detail_results = {}
        if detail_ids:
            tasks = [_get_details_safe(vid) for vid in detail_ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for vid, result in zip(detail_ids, results):
                if isinstance(result, dict):
                    detail_results[vid] = result

        vacancies = []
        for idx, item in enumerate(items):
            vacancy_id = item.get("id")
            requirements = []
            description_snippet = item.get("snippet", {}).get("requirement", "")

            if vacancy_id in detail_results:
                details = detail_results[vacancy_id]
                requirements = details.get("requirements", [])
                if details.get("description"):
                    description_snippet = details["description"][:500]

            if not requirements:
                snippet_text = description_snippet or ""
                if snippet_text:
                    clean_text = re.sub(r'<[^>]+>', '', snippet_text)
                    words = clean_text.split()[:15]
                    requirements = [w.strip('.,;:!?()') for w in words if len(w.strip('.,;:!?()')) > 3]

            vacancies.append({
                "id": vacancy_id,
                "title": item.get("name", "Без названия"),
                "company": item.get("employer", {}).get("name", "Не указана"),
                "salary": _format_salary(item.get("salary")),
                "url": item.get("alternate_url", ""),
                "location": item.get("area", {}).get("name", "") if item.get("area") else "",
                "description_snippet": description_snippet,
                "requirements": requirements,
                "published": item.get("published_at", ""),
            })

        # Сохраняем в кэш
        _hh_search_cache[cache_key] = {"data": vacancies, "time": time.time()}
        logger.info(f"HH search: {len(vacancies)} vacancies, cached")
        return vacancies


async def _get_details_safe(vacancy_id: str) -> dict:
    """Обёртка для get_vacancy_details без print"""
    return await get_vacancy_details(vacancy_id)


async def get_vacancy_details(vacancy_id: str) -> dict:
    """Детальная информация о вакансии"""
    headers = {"User-Agent": HH_USER_AGENT}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
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
    key_skills = vacancy_data.get("key_skills", [])
    return [skill.get("name", "") for skill in key_skills] if key_skills else []

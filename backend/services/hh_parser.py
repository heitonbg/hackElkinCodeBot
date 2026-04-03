import asyncio
import httpx
import json
import re
import os
from typing import List, Dict
from collections import Counter

# HH.ru API
HH_API_URL = "https://api.hh.ru/vacancies"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Роли для парсинга (на английском или транслитом)
ROLES_TO_PARSE = [
    {"role": "sales manager", "role_id": "sales"},
    {"role": "hr manager", "role_id": "hr"},
    {"role": "python developer", "role_id": "python_dev"},
    {"role": "data analyst", "role_id": "data_analyst"},
    {"role": "marketing manager", "role_id": "marketing"},
    {"role": "lawyer", "role_id": "lawyer"},
    {"role": "procurement specialist", "role_id": "procurement"},
    {"role": "telecom engineer", "role_id": "engineer"},
    {"role": "sales consultant", "role_id": "seller"},
]


async def search_vacancies(role: str, limit: int = 20) -> List[Dict]:
    """Поиск вакансий по роли"""
    async with httpx.AsyncClient(timeout=30) as client:
        params = {
            "text": role,
            "area": 113,  # Россия
            "per_page": limit,
            "search_field": "name",
        }
        headers = {"User-Agent": USER_AGENT}
        
        try:
            response = await client.get(HH_API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except Exception as e:
            print(f"   Ошибка поиска: {e}")
            return []


async def get_vacancy_description(vacancy_id: str) -> str:
    """Получение полного описания вакансии"""
    async with httpx.AsyncClient(timeout=30) as client:
        headers = {"User-Agent": USER_AGENT}
        try:
            response = await client.get(f"{HH_API_URL}/{vacancy_id}", headers=headers)
            response.raise_for_status()
            data = response.json()
            
            description = data.get("description", "")
            # Убираем HTML теги
            description = re.sub(r'<[^>]+>', ' ', description)
            
            key_skills = data.get("key_skills", [])
            skills_text = ", ".join([s["name"] for s in key_skills])
            
            return f"{description}\n\nКлючевые навыки: {skills_text}"
        except Exception as e:
            return ""


def extract_requirements(description: str) -> List[str]:
    """Извлекает требования из описания вакансии"""
    if not description:
        return []
    
    requirements = []
    
    # Ищем блоки с требованиями
    patterns = [
        r'(?:Требования|Необходимо|Обязательно|Навыки|Мы ждем от вас|Что нужно знать|Что требуется|Qualifications|Requirements)[\s:]*([^.\n]+[.,!;]?)',
        r'[•\-*]\s*([^.\n]+[.,!;]?)',
        r'\d+\.\s*([^.\n]+[.,!;]?)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            clean = match.strip()
            if 15 < len(clean) < 200 and not clean.startswith(('http', 'www')):
                requirements.append(clean)
    
    # Убираем дубликаты
    unique = list(dict.fromkeys(requirements))
    return unique[:10]


def extract_skills(description: str) -> List[str]:
    """Извлекает технические навыки из описания"""
    skill_keywords = [
        "python", "sql", "excel", "git", "docker", "linux", "java", "javascript",
        "react", "vue", "angular", "django", "flask", "fastapi", "pandas", "numpy",
        "power bi", "tableau", "1с", "oracle", "sap", "crm", "photoshop", "figma",
        "postgresql", "mysql", "mongodb", "kubernetes", "jenkins", "english",
        "коммуникация", "переговоры", "лидерство", "работа в команде"
    ]
    
    found = []
    desc_lower = description.lower()
    
    for skill in skill_keywords:
        if skill.lower() in desc_lower:
            found.append(skill.capitalize())
    
    return list(dict.fromkeys(found))[:10]


async def parse_all_roles() -> Dict:
    """Главная функция парсинга всех ролей"""
    results = {}
    
    for role_info in ROLES_TO_PARSE:
        role_name = role_info["role"]
        role_id = role_info["role_id"]
        
        print(f"🔍 Парсим: {role_name}...")
        
        try:
            # Ищем вакансии
            vacancies = await search_vacancies(role_name, limit=15)
            print(f"   Найдено вакансий: {len(vacancies)}")
            
            if not vacancies:
                print(f"   ⚠️ Вакансии не найдены, пропускаем")
                continue
            
            all_requirements = []
            all_skills = []
            
            for vac in vacancies[:10]:  # Берём первые 10
                desc = await get_vacancy_description(vac["id"])
                if desc:
                    reqs = extract_requirements(desc)
                    skills = extract_skills(desc)
                    all_requirements.extend(reqs)
                    all_skills.extend(skills)
            
            # Считаем частоту
            req_counter = Counter(all_requirements)
            skill_counter = Counter(all_skills)
            
            # Берём топ-10 требований и топ-10 навыков
            top_requirements = [{"text": req, "count": count} for req, count in req_counter.most_common(10)]
            top_skills = [{"skill": skill, "count": count} for skill, count in skill_counter.most_common(10)]
            
            results[role_id] = {
                "role_name": role_name,
                "requirements": top_requirements,
                "skills": top_skills,
                "total_parsed": len(all_requirements)
            }
            
            print(f"   ✅ Собрано {len(top_requirements)} требований, {len(top_skills)} навыков")
            
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            results[role_id] = {"error": str(e)}
        
        # Небольшая пауза, чтобы не забанили
        await asyncio.sleep(1)
    
    return results


async def save_to_json():
    """Сохраняет результаты в JSON файл"""
    # Создаём папку data относительно текущего файла
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    results = await parse_all_roles()
    
    filepath = os.path.join(data_dir, 'hh_requirements.json')
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Результаты сохранены в {filepath}")
    return results


if __name__ == "__main__":
    asyncio.run(save_to_json())
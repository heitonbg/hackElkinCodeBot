from services.ai_service import evaluate_match


async def match_vacancies(user_skills: list, vacancies: list) -> list:
    """Матчинг пользователя со списком вакансий"""
    matched = []
    
    for vacancy in vacancies:
        requirements = vacancy.get("requirements", [])
        
        if requirements:
            # AI оценка соответствия
            match_result = await evaluate_match(user_skills, requirements)
        else:
            # Базовый матчинг по названиям навыков
            match_result = _simple_match(user_skills, [])
        
        matched.append({
            "vacancy": vacancy,
            "match_score": match_result.get("match_score", 0),
            "missing_skills": match_result.get("missing_skills", []),
            "matching_skills": match_result.get("matching_skills", []),
            "recommendations": match_result.get("recommendations", []),
        })
    
    # Сортировка по % совпадения
    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return matched


def _simple_match(user_skills: list, requirements: list) -> dict:
    """Простой алгоритм матчинга без AI"""
    if not requirements:
        # Если нет требований, считаем по общим навыкам
        score = min(len(user_skills) * 10, 80)
        return {
            "match_score": score,
            "missing_skills": [],
            "matching_skills": user_skills[:3],
            "recommendations": ["Укажите больше навыков для точного матчинга"]
        }
    
    user_set = set(s.lower() for s in user_skills)
    req_set = set(s.lower() for s in requirements)
    
    matching = user_set & req_set
    missing = req_set - user_set
    
    score = round(len(matching) / len(req_set) * 100) if req_set else 0
    
    return {
        "match_score": score,
        "missing_skills": list(missing),
        "matching_skills": list(matching),
        "recommendations": [f"Изучи: {skill}" for skill in list(missing)[:3]]
    }

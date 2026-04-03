"""Матчинг пользователя с вакансиями МТС из матрицы компетенций"""

from services.mts_vacancies import get_all_mts_vacancies, get_it_vacancies
from services.ai_service import evaluate_match


# Ключевые слова для маппинга навыков пользователя на требования вакансий
SKILL_KEYWORDS = {
    "python": ["python", "программирование", "скрипты", "автоматизация"],
    "sql": ["sql", "базы данных", "данные", "аналитика", "bi"],
    "git": ["git", "контроль версий", "github", "gitlab"],
    "javascript": ["javascript", "js", "react", "vue", "angular", "frontend", "фронтенд"],
    "excel": ["excel", "таблицы", "ms office", "офис"],
    "английский": ["английский", "english"],
    "коммуникация": ["коммуникация", "переговоры", "общение", "презентации"],
    "лидерство": ["лидерство", "управление", "руководство", "менеджмент"],
    "ai": ["ai", "ml", "искусственный интеллект", "машинное обучение", "нейросети"],
    "аналитика": ["аналитика", "анализ", "метрики", "отчёты", "визуализация"],
    "продажи": ["продажи", "клиенты", "crm", "переговоры"],
    "hr": ["hr", "рекрутинг", "подбор", "резюме", "кандидаты"],
    "маркетинг": ["маркетинг", "реклама", "btl", "бренд", "продвижение"],
    "сети": ["сети", "tcp/ip", "cisco", "маршрутизация", "cкс"],
    "windows": ["windows", "microsoft", "администрирование", "сервер"],
    "дизайн": ["дизайн", "figma", "photoshop", "ui", "ux"],
    "devops": ["devops", "docker", "kubernetes", "ci/cd", "linux"],
    "тестирование": ["тестирование", "qa", "pytest", "автотесты"],
}


def match_user_to_mts_vacancies(user_skills: list, user_interests: list, only_it: bool = True):
    """
    Матчит навыки и интересы пользователя с вакансиями МТС.
    Возвращает отсортированный список вакансий с % совпадения.
    """
    vacancies = get_it_vacancies() if only_it else get_all_mts_vacancies()

    # Собираем все ключевые слова пользователя
    user_keywords = set()
    for skill in user_skills:
        skill_lower = skill.lower()
        # Добавляем сам навык
        user_keywords.add(skill_lower)
        # Добавляем связанные ключевые слова
        for mapped_skill, keywords in SKILL_KEYWORDS.items():
            if mapped_skill.lower() in skill_lower or skill_lower in mapped_skill.lower():
                user_keywords.update(keywords)

    # Добавляем интересы как ключевые слова
    for interest in user_interests:
        user_keywords.add(interest.lower())

    matched = []

    for vacancy in vacancies:
        # Собираем все требования и теги вакансии
        vac_text = " ".join(vacancy.get("requirements", [])).lower()
        vac_tags = [t.lower() for t in vacancy.get("tags", [])]
        vac_all_text = vac_text + " " + " ".join(vac_tags)

        # Считаем совпадения
        matching = []
        for keyword in user_keywords:
            if keyword in vac_all_text:
                matching.append(keyword)

        # Убираем дубликаты
        matching = list(set(matching))

        # Базовый скоринг: % совпадения ключевых слов
        total_keywords = len(set(vac_tags + [r.split()[0].lower() for r in vacancy.get("requirements", []) if r]))
        base_score = round(len(matching) / max(total_keywords, 1) * 100) if total_keywords > 0 else 0

        # Бонус за уровень опыта
        level_bonus = 0
        user_exp_text = " ".join(user_skills).lower() + " ".join(user_interests).lower()
        if "без опыта" in user_exp_text and vacancy.get("experience") == "Без опыта":
            level_bonus = 10
        elif "стаж" in user_exp_text and "intern" in vacancy.get("level", "").lower():
            level_bonus = 10
        elif "junior" in vacancy.get("level", "").lower():
            level_bonus = 5

        # Бонус за совпадение образования
        edu_bonus = 0
        # (упрощённо — можно расширить)

        final_score = min(base_score + level_bonus + edu_bonus, 95)

        # Определяем недостающие навыки (теги вакансии, которых нет у пользователя)
        missing = []
        for tag in vac_tags:
            if tag not in user_keywords:
                missing.append(tag)

        # Формируем рекомендации
        recommendations = []
        if missing:
            for m in missing[:3]:
                recommendations.append(f"Изучи: {m}")

        matched.append({
            "vacancy": vacancy,
            "match_score": final_score,
            "matching_skills": matching[:5],
            "missing_skills": missing[:5],
            "recommendations": recommendations,
        })

    # Сортируем по % совпадения
    matched.sort(key=lambda x: x["match_score"], reverse=True)
    return matched


def get_top_matches(user_skills: list, user_interests: list, top_n: int = 10):
    """Возвращает топ-N подходящих вакансий МТС"""
    all_matched = match_user_to_mts_vacancies(user_skills, user_interests, only_it=True)
    return all_matched[:top_n]

"""
Rule-based матчинг профессий — мгновенно, без AI.

Алгоритм:
1. Навыки пользователя vs required_skills роли (0-30 баллов)
2. Поле/образование пользователя vs category (0-30 баллов)
3. Интересы пользователя vs keywords категории (0-20 баллов)
4. Опыт пользователя (0-20 баллов)

Итого: 0-100 баллов. Сортировка по убыванию.
"""

import json
import os
import logging

logger = logging.getLogger(__name__)

ROLES_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'roles_database.json')
_roles_cache = None

# Эмодзи для категорий
CATEGORY_EMOJI = {
    "it_and_development": "💻", "data_and_analytics": "📊", "design_and_creative": "🎨",
    "marketing_and_sales": "📢", "management": "👔", "finance_and_accounting": "💰",
    "engineering_and_manufacturing": "⚙️", "media_and_entertainment": "🎬", "hospitality": "🏨",
    "hr_and_recruitment": "🤝", "logistics_and_supply_chain": "🚚", "legal": "⚖️",
    "telecom": "📡", "healthcare": "🏥", "education": "📚", "retail": "🛒",
    "construction": "🏗️", "science_and_research": "🔬", "beauty": "💅",
    "cleaning_and_services": "🧹", "security": "🔒", "sport": "⚽",
    "transport": "🚗", "energy": "⚡", "social_work": "❤️", "non_profit": "🌍",
    "real_estate": "🏠", "agriculture": "🌾", "customer_service": "🎧",
    "automotive": "🚙", "crafts": "🔨",
}

# Маппинг полей образования → категории ролей
FIELD_CATEGORY_MAP = {
    "it и программирование": ["it_and_development", "data_and_analytics"],
    "аналитика и данные": ["data_and_analytics", "it_and_development"],
    "дизайн и креатив": ["design_and_creative", "media_and_entertainment"],
    "маркетинг и продажи": ["marketing_and_sales", "retail"],
    "управление": ["management", "non_profit"],
    "hr и рекрутинг": ["hr_and_recruitment", "management"],
    "финансы и экономика": ["finance_and_accounting", "logistics_and_supply_chain"],
    "юриспруденция и право": ["legal", "security"],
    "инженерия и телеком": ["engineering_and_manufacturing", "telecom", "energy"],
    "медицина": ["healthcare", "science_and_research"],
    "образование": ["education", "training_coordinator"],
    "строительство": ["construction", "engineering_and_manufacturing"],
    "сельское хозяйство": ["agriculture", "food_technologist"],
    "транспорт": ["transport", "logistics_and_supply_chain"],
    "гостиничный бизнес": ["hospitality", "retail"],
    "спорт": ["sport", "healthcare"],
    "бьюти": ["beauty", "retail"],
    "администрирование": ["cleaning_and_services", "management", "customer_service"],
}

# Ключевые слова интересов → категории
INTEREST_KEYWORDS = {
    "it и программирование": {"программирован", "код", "разработк", "it", "сайт", "приложен", "софт", "технолог"},
    "аналитика и данные": {"аналитик", "данны", "data", "статистик", "метри", "отчёт", "цифр"},
    "дизайн и креатив": {"дизайн", "креатив", "рисован", "визуал", "эстетик", "красив", "творчеств"},
    "маркетинг и продажи": {"маркетинг", "продаж", "реклам", "бренд", "продвиж", "клиент"},
    "управление": {"управлен", "лидерств", "команд", "стратеги", "руководств"},
    "hr и рекрутинг": {"hr", "рекрутинг", "подбор", "люди", "персонал", "команд"},
    "финансы и экономика": {"финанс", "экономик", "инвестиц", "бухгалтер", "деньг", "банк"},
    "юриспруденция и право": {"юриспруденц", "право", "закон", "суд", "юрист", "правов"},
    "инженерия и телеком": {"инженери", "телеком", "сети", "оборудован", "монтаж", "строител"},
    "медицина": {"медицин", "здоровь", "фармац", "врач", "лечен", "биолог"},
    "образование": {"образован", "преподаван", "обучен", "учеб", "педагогик"},
    "строительство": {"строител", "архитектур", "проект", "ремонт"},
    "сельское хозяйство": {"сельск", "агро", "фермер", "растен", "животн"},
    "транспорт": {"транспорт", "логистик", "доставк", "воджен"},
    "гостиничный бизнес": {"гостиниц", "отел", "ресторан", "туризм", "сервис"},
    "спорт": {"спорт", "фитнес", "тренировк", "здоров"},
    "бьюти": {"бьюти", "красот", "стиль", "мода", "уход"},
    "администрирование": {"администрирован", "офис", "документ", "порядок", "организ"},
}


def _load_roles_db():
    """Загрузка БД ролей с кэшированием"""
    global _roles_cache
    if _roles_cache is None:
        try:
            with open(ROLES_DB_PATH, 'r', encoding='utf-8') as f:
                _roles_cache = json.load(f)
            logger.info(f"📚 Roles DB loaded: {_roles_cache['total_roles']} roles")
        except Exception as e:
            logger.error(f"Failed to load roles DB: {e}")
            _roles_cache = {"roles": [], "total_roles": 0}
    return _roles_cache


def match_roles(user_data: dict) -> list:
    """
    Rule-based матчинг ролей под профиль пользователя.
    
    Args:
        user_data: {
            "education": str,
            "field": str,
            "experience": str,
            "interests": [str],
            "skills": [str],
            "career_goals": [str],
        }
    
    Returns:
        [{"role_id": str, "title": str, "category": str, "match_percent": int, "reason": str, "skills": [str], "salary": {}}]
    """
    db = _load_roles_db()
    roles = db.get("roles", [])

    user_skills = [s.strip().lower() for s in user_data.get("skills", []) if s]
    user_interests = [i.lower() for i in user_data.get("interests", []) if i]
    user_field = user_data.get("field", "").lower()
    user_experience = user_data.get("experience", "").lower()

    results = []

    for role in roles:
        score = 0
        matched_skills = []
        reasons = []

        # 1. Навыки (0-30 баллов)
        role_skills = [s.lower() for s in role.get("skills", [])]
        for us in user_skills:
            for rs in role_skills:
                if us == rs or us in rs or rs in us:
                    matched_skills.append(role["skills"][role_skills.index(rs)])
                    score += 5  # 6 навыков × 5 = 30 макс
                    break
        score = min(score, 30)

        # 2. Поле/образование (0-30 баллов)
        role_cat = role.get("category_id", "")
        if user_field:
            for field_kw, cats in FIELD_CATEGORY_MAP.items():
                if field_kw in user_field and role_cat in cats:
                    score += 30
                    reasons.append(f"Совпадение по направлению: {field_kw}")
                    break

        # 3. Интересы (0-20 баллов)
        for interest in user_interests:
            for field_kw, keywords in INTEREST_KEYWORDS.items():
                for kw in keywords:
                    if kw in interest:
                        # Проверяем, относится ли роль к этой категории
                        for fkw, cats in FIELD_CATEGORY_MAP.items():
                            if fkw == field_kw and role_cat in cats:
                                score += 10
                                reasons.append(f"Интерес: {interest}")
                                break
                        break
                else:
                    continue
                break
        score = min(score, 20)

        # 4. Опыт (0-20 баллов)
        exp_keywords = {
            "нет опыта": 5,
            "менее года": 10,
            "1-2 года": 15,
            "2-3 года": 18,
            "3-5 лет": 20,
            "более 5 лет": 20,
        }
        for kw, val in exp_keywords.items():
            if kw in user_experience:
                score += val
                break

        # Минимальный порог — показываем только релевантные
        if score >= 10:
            reason = ", ".join(reasons[:2]) if reasons else "Может подойти по профилю"
            if matched_skills:
                reason = f"Навыки: {', '.join(matched_skills[:3])}" + (f"; {reason}" if reasons else "")

            results.append({
                "role_id": role["role_id"],
                "title": role["title"],
                "category": role["category"],
                "category_emoji": CATEGORY_EMOJI.get(role.get("category_id", ""), "💼"),
                "match_percent": min(score, 95),
                "reason": reason,
                "skills": role.get("skills", []),
                "salary": role.get("salary", {}),
                "scenarios_available": list(role.get("scenarios", {}).keys()),
            })

    # Сортировка по match_percent
    results.sort(key=lambda x: x["match_percent"], reverse=True)

    # Если ничего не нашлось (профиль пустой) — возвращаем популярные роли для демо
    if not results:
        logger.info("No roles matched, returning popular roles for demo")
        popular_role_ids = [
            "python_dev", "frontend_dev", "data_analyst", "devops_engineer",
            "digital_marketer", "project_manager", "ux_designer", "sales_manager_b2b",
        ]
        for role in roles:
            if role["role_id"] in popular_role_ids:
                results.append({
                    "role_id": role["role_id"],
                    "title": role["title"],
                    "category": role["category"],
                    "match_percent": 0,
                    "reason": "Популярная роль (попробуй пройти тест!)",
                    "skills": role.get("skills", []),
                    "salary": role.get("salary", {}),
                    "scenarios_available": list(role.get("scenarios", {}).keys()),
                })

    # Топ-12
    return results[:12]


def get_all_roles() -> list:
    """Возвращает все роли из БД (для поиска)"""
    db = _load_roles_db()
    return db.get("roles", [])


def search_roles(query: str) -> list:
    """Поиск ролей по названию (мгновенно)"""
    db = _load_roles_db()
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    results = []
    for role in db.get("roles", []):
        if query_lower in role["title"].lower() or query_lower in role["category"].lower():
            results.append({
                "role_id": role["role_id"],
                "title": role["title"],
                "category": role["category"],
                "skills": role.get("skills", []),
                "salary": role.get("salary", {}),
                "scenarios_available": list(role.get("scenarios", {}).keys()),
            })
    return results[:20]


def get_role_scenario(role_id: str, level: str = "junior") -> dict | None:
    """Получить сценарий для роли и уровня.
    Ищет сначала в scenarios_primary.json, потом в scenarios_from_hh.json.
    """
    # Сначала ищем в scenarios_primary.json
    scenarios_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_primary.json'),
        os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_from_hh.json'),
    ]
    
    for path in scenarios_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for scenario in data.get("scenarios", []):
                if scenario.get("role_id") == role_id:
                    return {
                        "role_id": scenario["role_id"],
                        "title": scenario.get("title") or scenario.get("role_name", ""),
                        "questions": scenario.get("questions", []),
                    }
        except Exception as e:
            logger.warning(f"Failed to load scenarios from {path}: {e}")
    
    # Если не нашли в отдельных файлах — ищем в roles_database.json
    db = _load_roles_db()
    for role in db.get("roles", []):
        if role["role_id"] == role_id:
            scenarios = role.get("scenarios", {})
            if level in scenarios:
                return {
                    "role_id": role["role_id"],
                    "title": role["title"],
                    **scenarios[level],
                }
    
    return None

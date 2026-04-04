"""
Диагностический скоринг — определяет подходящие профессии на основе ответов пользователя.

Алгоритм:
1. Загружаем 10 диагностических вопросов
2. Считаем баллы по категориям на основе ответов
3. Возвращаем топ-N категорий с баллами
4. Маппим категории на роли из roles_database.json
"""

import json
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'diagnostic_questions.json')
ROLES_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'roles_database.json')

_questions_cache = None
_roles_cache = None

# Маппинг category_id → category (название из roles_database) + эмодзи
CATEGORY_EMOJI = {
    "it_and_development": "💻",
    "data_and_analytics": "📊",
    "design_and_creative": "🎨",
    "marketing_and_sales": "📢",
    "management": "👔",
    "finance_and_accounting": "💰",
    "engineering_and_manufacturing": "⚙️",
    "media_and_entertainment": "🎬",
    "hospitality": "🏨",
    "hr_and_recruitment": "🤝",
    "logistics_and_supply_chain": "🚚",
    "legal": "⚖️",
    "telecom": "📡",
    "healthcare": "🏥",
    "education": "📚",
    "retail": "🛒",
    "construction": "🏗️",
    "science_and_research": "🔬",
    "beauty": "💅",
    "cleaning_and_services": "🧹",
    "security": "🔒",
    "sport": "⚽",
    "transport": "🚗",
    "energy": "⚡",
    "social_work": "❤️",
    "non_profit": "🌍",
    "real_estate": "🏠",
    "agriculture": "🌾",
    "customer_service": "🎧",
    "automotive": "🚙",
    "crafts": "🔨",
}

CATEGORY_ID_TO_NAME = {
    "it_and_development": "IT и разработка",
    "data_and_analytics": "Аналитика и данные",
    "design_and_creative": "Дизайн и креатив",
    "marketing_and_sales": "Маркетинг и продажи",
    "management": "Управление",
    "finance_and_accounting": "Финансы и бухгалтерия",
    "engineering_and_manufacturing": "Инженерия и производство",
    "media_and_entertainment": "Медиа и развлечения",
    "hospitality": "Гостиничный бизнес и рестораны",
    "hr_and_recruitment": "HR и рекрутинг",
    "logistics_and_supply_chain": "Логистика и цепочки поставок",
    "legal": "Юриспруденция",
    "telecom": "Телекоммуникации",
    "healthcare": "Медицина и фармацевтика",
    "education": "Образование",
    "retail": "Ритейл и торговля",
    "construction": "Строительство",
    "science_and_research": "Наука и исследования",
    "beauty": "Бьюти-индустрия",
    "cleaning_and_services": "Клининг и услуги",
    "security": "Безопасность",
    "sport": "Спорт и фитнес",
    "transport": "Транспорт",
    "energy": "Энергетика",
    "social_work": "Социальная работа",
    "non_profit": "НКО и благотворительность",
    "real_estate": "Недвижимость",
    "agriculture": "Сельское хозяйство",
    "customer_service": "Обслуживание клиентов",
    "automotive": "Автомобильная отрасль",
    "crafts": "Ремёсла и производство",
}


def _load_questions():
    """Загрузка вопросов с кэшированием"""
    global _questions_cache
    if _questions_cache is None:
        try:
            with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
                _questions_cache = json.load(f)
            logger.info(f"📋 Diagnostic questions loaded: {len(_questions_cache['questions'])} questions")
        except Exception as e:
            logger.error(f"Failed to load diagnostic questions: {e}")
            _questions_cache = {"questions": []}
    return _questions_cache


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


def get_diagnostic_questions() -> list:
    """Вернуть все вопросы для фронтенда"""
    data = _load_questions()
    return data.get("questions", [])


def score_diagnostic(answers: List[Dict[str, str]]) -> Dict:
    """
    Подсчитать баллы по категориям на основе ответов.

    Args:
        answers: [{"question_id": "q1", "answer": "Создавать что-то новое с нуля"}, ...]

    Returns:
        {
            "top_categories": [{"category_id": str, "category_name": str, "score": int}, ...],
            "recommended_roles": [{"role_id": str, "title": str, "category": str, "match_percent": int, "reason": str}, ...]
        }
    """
    questions_data = _load_questions()
    questions = questions_data.get("questions", [])

    # Считаем баллы по категориям
    category_scores = {}

    for answer in answers:
        q_id = answer.get("question_id")
        answer_text = answer.get("answer")

        # Находим вопрос
        question = next((q for q in questions if q["id"] == q_id), None)
        if not question:
            continue

        # Находим выбранный ответ
        option = next((o for o in question["options"] if o["text"] == answer_text), None)
        if not option:
            continue

        # Добавляем баллы по категориям
        scores = option.get("scores", {})
        for cat_id, points in scores.items():
            category_scores[cat_id] = category_scores.get(cat_id, 0) + points

    # Сортируем категории по баллам
    sorted_categories = sorted(category_scores.items(), key=lambda x: -x[1])

    # Нормализуем баллы в проценты (макс балл = 10 вопросов × 10 баллов = 100)
    max_possible = 100
    top_categories = []
    for cat_id, score in sorted_categories[:10]:  # топ-10 категорий
        percent = min(round((score / max_possible) * 100), 95)
        if percent > 0:
            top_categories.append({
                "category_id": cat_id,
                "category_name": CATEGORY_ID_TO_NAME.get(cat_id, cat_id),
                "score": percent,
            })

    # Получаем рекомендованные роли из топ-5 категорий
    top_category_ids = [c["category_id"] for c in top_categories[:5]]
    recommended_roles = _get_roles_for_categories(top_category_ids, category_scores)

    return {
        "top_categories": top_categories,
        "recommended_roles": recommended_roles[:12],  # топ-12 ролей
        "total_questions": len(questions),
        "answered_questions": len(answers),
    }


def _get_roles_for_categories(category_ids: List[str], category_scores: Dict) -> List[Dict]:
    """Получить роли для заданных категорий, отсортированные по релевантности"""
    roles_db = _load_roles_db()
    all_roles = roles_db.get("roles", [])

    results = []
    for role in all_roles:
        role_cat_id = role.get("category_id", "")
        if role_cat_id in category_ids:
            # Базовый процент из категории
            base_score = category_scores.get(role_cat_id, 0)
            percent = min(round((base_score / 100) * 100), 95)

            if percent >= 5:  # минимальный порог
                emoji = CATEGORY_EMOJI.get(role_cat_id, "💼")
                results.append({
                    "role_id": role["role_id"],
                    "title": role["title"],
                    "category": role["category"],
                    "category_emoji": emoji,
                    "match_percent": percent,
                    "reason": f"Подходит по направлению: {role['category']}",
                    "skills": role.get("skills", []),
                    "salary": role.get("salary", {}),
                    "scenarios_available": list(role.get("scenarios", {}).keys()),
                })

    # Сортировка по match_percent
    results.sort(key=lambda x: x["match_percent"], reverse=True)
    return results


def save_diagnostic_result(telegram_id: str, answers: List[Dict], results: Dict):
    """Сохранить результаты диагностики в БД (можно доработать)"""
    # TODO: сохранить в БД историю диагностик
    logger.info(f"Diagnostic saved for {telegram_id}: {len(answers)} answers, {len(results['recommended_roles'])} roles")

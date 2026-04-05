"""
Achievement System — бейджи за достижения.
Проверяет условия и выдаёт бейджи.
"""
import logging
from database.db import db

logger = logging.getLogger(__name__)

# Определение всех бейджей
ACHIEVEMENTS = {
    # Первые шаги
    "first_diagnostic": {
        "emoji": "🎯",
        "title": "Первый шаг",
        "desc": "Пройди диагностику",
    },
    "first_test": {
        "emoji": "✅",
        "title": "Испытатель",
        "desc": "Пройди первый тест по роли",
    },
    "first_daily": {
        "emoji": "🎭",
        "title": "Ежедневник",
        "desc": "Реши первый Daily Challenge",
    },

    # Streak
    "streak_3": {
        "emoji": "🔥",
        "title": "На огне",
        "desc": "3 дня Daily Challenge подряд",
    },
    "streak_7": {
        "emoji": "💥",
        "title": "Неделя подряд",
        "desc": "7 дней Daily Challenge подряд",
    },
    "streak_30": {
        "emoji": "🌟",
        "title": "Марафонец",
        "desc": "30 дней Daily Challenge подряд",
    },

    # Тесты
    "tests_5": {
        "emoji": "📚",
        "title": "Знаток",
        "desc": "Пройди 5 тестов по разным ролям",
    },
    "tests_10": {
        "emoji": "🎓",
        "title": "Эрудит",
        "desc": "Пройди 10 тестов по разным ролям",
    },

    # Результаты
    "perfect_score": {
        "emoji": "💯",
        "title": "Перфекционист",
        "desc": "Получи 90%+ в любом тесте",
    },
    "high_avg": {
        "emoji": "⭐",
        "title": "Звезда",
        "desc": "Средний балл 80%+ по всем тестам",
    },

    # Daily Challenge — отличные ответы
    "daily_excellent": {
        "emoji": "🏆",
        "title": "Отличник",
        "desc": "Получи 8/10+ в Daily Challenge",
    },
    "daily_perfect": {
        "emoji": "👑",
        "title": "Король знаний",
        "desc": "Получи 10/10 в Daily Challenge",
    },

    # Профиль
    "full_profile": {
        "emoji": "👤",
        "title": "Открытая книга",
        "desc": "Заполни профиль на 100%",
    },

    # Исследователь
    "explore_3_roles": {
        "emoji": "🔍",
        "title": "Исследователь",
        "desc": "Попробуй 3 разные роли",
    },
}


async def check_and_unlock(telegram_id: str, achievement_id: str) -> bool:
    """Проверить и разблокировать если условие выполнено"""
    if achievement_id not in ACHIEVEMENTS:
        return False
    
    already = await db.has_achievement(telegram_id, achievement_id)
    if already:
        return False

    unlocked = await db.unlock_achievement(telegram_id, achievement_id)
    if unlocked:
        logger.info(f"🏆 Achievement unlocked: {achievement_id} for {telegram_id}")
        return True
    return False


async def check_test_achievements(telegram_id: str, role_id: str, score: int, total_tests: int, unique_roles: int, avg_score: float):
    """Проверить достижения после теста"""
    new = []
    
    # Первый тест
    if total_tests >= 1:
        if await check_and_unlock(telegram_id, "first_test"):
            new.append(ACHIEVEMENTS["first_test"])
    
    # 5 тестов
    if total_tests >= 5:
        if await check_and_unlock(telegram_id, "tests_5"):
            new.append(ACHIEVEMENTS["tests_5"])
    
    # 10 тестов
    if total_tests >= 10:
        if await check_and_unlock(telegram_id, "tests_10"):
            new.append(ACHIEVEMENTS["tests_10"])
    
    # 90%+
    if score >= 90:
        if await check_and_unlock(telegram_id, "perfect_score"):
            new.append(ACHIEVEMENTS["perfect_score"])
    
    # Средний 80%+
    if avg_score >= 80:
        if await check_and_unlock(telegram_id, "high_avg"):
            new.append(ACHIEVEMENTS["high_avg"])
    
    # 3 разные роли
    if unique_roles >= 3:
        if await check_and_unlock(telegram_id, "explore_3_roles"):
            new.append(ACHIEVEMENTS["explore_3_roles"])
    
    return new


async def check_daily_achievements(telegram_id: str, score: int, streak: int, best_streak: int, total_daily: int):
    """Проверить достижения после Daily Challenge"""
    new = []
    
    # Первый daily
    if total_daily >= 1:
        if await check_and_unlock(telegram_id, "first_daily"):
            new.append(ACHIEVEMENTS["first_daily"])
    
    # Streak 3
    if streak >= 3:
        if await check_and_unlock(telegram_id, "streak_3"):
            new.append(ACHIEVEMENTS["streak_3"])
    
    # Streak 7
    if streak >= 7:
        if await check_and_unlock(telegram_id, "streak_7"):
            new.append(ACHIEVEMENTS["streak_7"])
    
    # Streak 30
    if streak >= 30:
        if await check_and_unlock(telegram_id, "streak_30"):
            new.append(ACHIEVEMENTS["streak_30"])
    
    # 8/10+
    if score >= 8:
        if await check_and_unlock(telegram_id, "daily_excellent"):
            new.append(ACHIEVEMENTS["daily_excellent"])
    
    # 10/10
    if score >= 10:
        if await check_and_unlock(telegram_id, "daily_perfect"):
            new.append(ACHIEVEMENTS["daily_perfect"])
    
    return new


async def check_profile_achievements(telegram_id: str, completeness: int):
    """Проверить достижения профиля"""
    new = []
    
    if completeness >= 100:
        if await check_and_unlock(telegram_id, "full_profile"):
            new.append(ACHIEVEMENTS["full_profile"])
    
    return new


async def check_diagnostic_achievement(telegram_id: str):
    """Проверить достижение диагностики"""
    new = []
    if await check_and_unlock(telegram_id, "first_diagnostic"):
        new.append(ACHIEVEMENTS["first_diagnostic"])
    return new


def get_all_achievements():
    """Вернуть все определения бейджей"""
    return ACHIEVEMENTS

"""
AI сервис для Daily Challenges.
Генерация ситуаций и оценка ответов.
"""
import json
import logging
from services.ai_service import _call_openai_with_fallback

logger = logging.getLogger(__name__)

DAILY_CHALLENGE_PROMPT = """
Ты — эксперт по карьерному развитию для роли "{role_title}" в компании МТС.

Создай реалистичную рабочую ситуацию (кейс), которую мог бы встретить специалист на позиции "{role_title}" (junior/middle уровень).

Ситуация должна:
- Быть конкретной и жизненной
- Требовать развёрнутого ответа (не да/нет)
- Проверять профессиональные навыки и soft skills
- Быть решаемой за 2-3 предложения

Верни ТОЛЬКО JSON:
{{
    "situation": "Текст ситуации (3-5 предложений)",
    "ideal_keywords": ["ключевое слово 1", "ключевое слово 2", "ключевое слово 3"]
}}

ideal_keywords — 3-5 ключевых идей/действий, которые ожидаются в хорошем ответе.
"""

EVALUATE_ANSWER_PROMPT = """
Ты — эксперт по оценке профессиональных компетенций.

Ситуация для роли "{role_title}":
{situation}

Ожидаемые ключевые идеи в ответе:
{ideal_keywords}

Ответ пользователя:
{user_answer}

Оцени ответ по шкале 1-10, где:
- 1-3: Ответ не по делу или слишком поверхностный
- 4-5: Базовое понимание, но не хватает глубины
- 6-7: Хороший ответ, есть практическое понимание
- 8-9: Отличный ответ с профессиональным подходом
- 10: Идеальный ответ уровня senior специалиста

Верни ТОЛЬКО JSON:
{{
    "score": 7,
    "feedback": "Конкретный фидбек: что хорошо, что можно улучшить (2-3 предложения)"
}}
"""


async def generate_daily_challenge(role_id: str, role_title: str) -> dict:
    """Сгенерировать ситуацию для daily challenge"""
    try:
        result = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты эксперт по карьерному развитию. Отвечай только JSON."},
                {"role": "user", "content": DAILY_CHALLENGE_PROMPT.format(role_title=role_title)},
            ],
            temperature=0.8,
            max_tokens=500,
        )

        # Парсим JSON из ответа
        content = result.strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        data = json.loads(content)
        return {
            "situation": data.get("situation", ""),
            "ideal_keywords": data.get("ideal_keywords", []),
        }
    except Exception as e:
        logger.error(f"Error generating daily challenge: {e}")
        # Fallback — запасная ситуация
        return {
            "situation": f"Вы работаете как {role_title}. Ваш руководитель просит подготовить отчёт о проделанной работе за неделю. Опишите, как вы подойдёте к этой задаче?",
            "ideal_keywords": ["структура", "метрики", "результаты", "планы"],
        }


async def evaluate_daily_answer(role_title: str, situation: str, ideal_keywords: list, user_answer: str) -> dict:
    """Оценить ответ пользователя"""
    try:
        keywords_str = ", ".join([f'"{kw}"' for kw in ideal_keywords]) if ideal_keywords else "профессиональный подход, конкретика, практическое решение"

        result = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты эксперт по оценке компетенций. Отвечай только JSON."},
                {"role": "user", "content": EVALUATE_ANSWER_PROMPT.format(
                    role_title=role_title,
                    situation=situation,
                    ideal_keywords=keywords_str,
                    user_answer=user_answer,
                )},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        # Парсим JSON
        content = result.strip()
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        data = json.loads(content)
        return {
            "score": min(10, max(1, int(data.get("score", 5)))),
            "feedback": data.get("feedback", "Хорошая попытка! Продолжай практиковаться."),
        }
    except Exception as e:
        logger.error(f"Error evaluating daily answer: {e}")
        return {
            "score": 5,
            "feedback": "Интересный ответ! Попробуй добавить больше конкретных деталей и профессиональных терминов.",
        }

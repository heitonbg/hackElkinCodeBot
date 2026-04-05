"""
Фоновый AI-анализ после прохождения сценариев.

После прохождения сценария пользователь мгновенно получает rule-based результат.
AI-анализ запускается в фоне и сохраняет расширенные рекомендации в БД.
"""

import asyncio
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_ai_client = None

def _get_ai_client():
    global _ai_client
    if _ai_client is None:
        try:
            from openai import AsyncOpenAI
            from dotenv import load_dotenv
            import os
            load_dotenv()
            key = os.getenv("OPENROUTER_API_KEY", "")
            if key:
                _ai_client = AsyncOpenAI(api_key=key, base_url="https://openrouter.ai/api/v1")
                logger.info("✅ AI-анализер подключен к OpenRouter")
            else:
                logger.warning("⚠️ OPENROUTER_API_KEY не установлен")
        except Exception as e:
            logger.error(f"AI client init error: {e}")
    return _ai_client


async def analyze_scenario_results(telegram_id: str, role_id: str, scenario_result: dict, user_profile: dict):
    """
    AI-анализ результатов сценария в фоне.
    
    Args:
        telegram_id: ID пользователя
        role_id: ID роли
        scenario_result: {"match_score": int, "details": [...], "level_label": str}
        user_profile: {"education": str, "field": str, "experience": str, "skills": [str]}
    """
    client = _get_ai_client()
    if not client:
        logger.info("AI недоступен, пропускаем фоновый анализ")
        return

    prompt = f"""
Проанализируй результаты тестирования пользователя.

Роль: {role_id}
Результат: {scenario_result['match_score']}% ({scenario_result['level_label']})
Профиль пользователя:
- Образование: {user_profile.get('education', 'не указано')}
- Направление: {user_profile.get('field', 'не указано')}
- Опыт: {user_profile.get('experience', 'не указан')}
- Навыки: {', '.join(user_profile.get('skills', [])) or 'не указаны'}

Детали ответов:
{json.dumps(scenario_result.get('details', []), ensure_ascii=False, indent=2)}

Верни СТРОГО JSON:
{{
    "strengths": ["конкретная сильная сторона 1", "конкретная сильная сторона 2"],
    "weaknesses": ["конкретное слабое место 1", "конкретное слабое место 2"],
    "recommendations": ["конкретная рекомендация 1", "конкретная рекомендация 2", "конкретная рекомендация 3"],
    "next_role_suggestion": "какую роль попробовать следующей",
    "feedback": "Короткий общий фидбек (2-3 предложения, на русском)"
}}
"""
    try:
        logger.info(f"🧠 Фоновый AI-анализ для {telegram_id} → {role_id}")
        response = await client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",  # Быстрая модель
            messages=[
                {"role": "system", "content": "Отвечай СТРОГО JSON на русском языке."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600,
            timeout=30,
        )
        content = response.choices[0].message.content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)

        # Сохраняем в БД
        from database.db import db
        await db.save_ai_analysis(telegram_id, role_id, result)
        logger.info(f"✅ AI-анализ сохранён для {telegram_id} → {role_id}")
        return result
    except Exception as e:
        logger.warning(f"Фоновый AI-анализ не удался: {e}")
        return None


async def generate_career_recommendations(telegram_id: str, user_profile: dict, scenario_results: list):
    """
    AI генерация карьерных рекомендаций на основе всех пройденных сценариев.
    """
    client = _get_ai_client()
    if not client:
        return None

    results_summary = json.dumps([
        {"role": r.get("role_id"), "score": r.get("match_score")}
        for r in scenario_results
    ], ensure_ascii=False)

    prompt = f"""
На основе результатов тестирования дай карьерные рекомендации.

Профиль:
- Образование: {user_profile.get('education', 'не указано')}
- Направление: {user_profile.get('field', 'не указано')}
- Опыт: {user_profile.get('experience', 'не указан')}
- Навыки: {', '.join(user_profile.get('skills', [])) or 'не указаны'}

Результаты тестирования:
{results_summary}

Верни СТРОГО JSON:
{{
    "top_career_paths": [
        {"path": "название пути", "description": "описание", "next_steps": ["шаг 1", "шаг 2"]}
    ],
    "key_skills_to_develop": ["навык 1", "навык 2", "навык 3"],
    "career_advice": "Общий совет по развитию карьеры (3-4 предложения)"
}}
"""
    try:
        response = await client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",
            messages=[
                {"role": "system", "content": "Отвечай СТРОГО JSON на русском языке."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=800,
            timeout=30,
        )
        content = response.choices[0].message.content.strip().strip("```json").strip("```").strip()
        return json.loads(content)
    except Exception as e:
        logger.warning(f"Career recommendations error: {e}")
        return None

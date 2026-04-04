import os
import json
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Загружаем .env из корня проекта
_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "qwen/qwen3.6-plus:free")
OPENROUTER_MODEL_FALLBACK = os.getenv("OPENROUTER_MODEL_FALLBACK", "stepfun/step-3.5-flash:free")

# Быстрая модель для простых задач (генерация ролей) — 2-5 сек
FAST_MODEL = "stepfun/step-3.5-flash:free"
# Качественная модель для сложных задач (сценарии, анализ) — 10-20 сек
QUALITY_MODEL = OPENROUTER_MODEL

# OpenRouter использует OpenAI-compatible API
openai_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
) if OPENROUTER_API_KEY else None

if not openai_client:
    logger.warning("⚠️ OpenRouter API key не установлен. AI будет использовать демо-данные.")
else:
    logger.info(f"✅ OpenRouter API подключен | Модель: {OPENROUTER_MODEL} | Fallback: {OPENROUTER_MODEL_FALLBACK}")


async def _call_openai_with_fallback(**kwargs) -> str:
    """Вызов OpenRouter с автоматическим fallback на другую модель"""
    # Пробуем основную модель
    try:
        kwargs["model"] = OPENROUTER_MODEL
        response = await openai_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_msg = str(e)
        logger.warning(f"Основная модель {OPENROUTER_MODEL} недоступна: {error_msg}")
        logger.info(f"Переключаюсь на fallback: {OPENROUTER_MODEL_FALLBACK}")
        
        # Пробуем fallback
        try:
            kwargs["model"] = OPENROUTER_MODEL_FALLBACK
            response = await openai_client.chat.completions.create(**kwargs)
            logger.info(f"✅ Fallback модель {OPENROUTER_MODEL_FALLBACK} работает")
            return response.choices[0].message.content.strip()
        except Exception as fallback_error:
            logger.error(f"Fallback модель тоже не работает: {fallback_error}")
            raise e  # Пробрасываем оригинальную ошибку

PROMPT_CAREER_ANALYSIS = """
Ты — ведущий IT-карьерный консультант с 15-летним опытом найма. Ты знаешь рынок изнутри и понимаешь, какие навыки нужны для каждой роли.

ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:
- Образование: {education}
- Направление: {field}
- Опыт: {experience}
- Интересы: {interests}
- Навыки: {skills}
- Карьерные цели: {career_goals}

ЗАДАЧА: Дай МАКСИМАЛЬНО КОНКРЕТНЫЕ рекомендации, привязанные к ЭТОМУ человеку. НЕ общие фразы.

Верни СТРОГО JSON:
{{
    "profile_summary": "Живой, конкретный анализ. НЕ начинай с 'Пользователь'. Пиши как живой человек. 2-3 предложения.",
    "personality_type": "Конкретный профиль: например 'Python-разработчик с уклоном в AI', 'Data Analyst', 'Fullstack Developer'",
    "strengths": ["конкретная сильная сторона 1", "конкретная сильная сторона 2", "конкретная сильная сторона 3", "конкретная сильная сторона 4"],
    "professions": [
        {{
            "title": "конкретная должность",
            "match_percent": число 40-95,
            "reason": "ПОЧЕМУ именно ЭТОМУ человеку. Ссылайся на его навыки, интересы, опыт, образование. 2-3 предложения.",
            "salary_range": "от X до Y ₽"
        }}
    ],
    "career_path": [
        {{
            "step": 1,
            "title": "конкретный этап",
            "description": "ЧТО ДЕЛАТЬ, КАКИЕ технологии учить, КАКИЕ проекты делать, ГДЕ учиться. Максимальная конкретика.",
            "duration": "X месяцев"
        }}
    ],
    "missing_skills": ["конкретный навык/технология 1", "конкретный навык 2", "конкретный навык 3", "конкретный навык 4", "конкретный навык 5"],
    "recommendations": [
        "КОНКРЕТНАЯ рекомендация: название КУРСА + платформа + что делать. Например: 'Пройди курс FastAPI на Stepik, сделай REST API с авторизацией'",
        "КОНКРЕТНАЯ рекомендация: ПРОЕКТ + технологии + где применить",
        "КОНКРЕТНАЯ рекомендация: СООБЩЕСТВА + КОНФЕРЕНЦИИ + нетворкинг",
        "КОНКРЕТНАЯ рекомендация: ПОРТФОЛИО + РЕЗЮМЕ + подготовка к собеседованиям"
    ]
}}

СТРОГИЕ ТРЕБОВАНИЯ:
1. МИНИМУМ 5 профессий с подробными причинами
2. МИНИМУМ 4 шага карьерного пути
3. МИНИМУМ 5 недостающих навыков
4. МИНИМУМ 4 рекомендации
5. Каждая рекомендация — ДЕЙСТВИЕ: КУРС (название+платформа), ПРОЕКТ, ТЕХНОЛОГИИ
6. Реальные зарплаты для России 2025
7. Привязывайся к КОНКРЕТНЫМ данным пользователя
8. НЕ используй шаблонные фразы вроде 'Пользователь имеет', 'является', 'обладает'

Ответ ТОЛЬКО JSON.
"""

PROMPT_CHAT = """
Ты — дружелюбный карьерный наставник с глубокими знаниями IT-рынка.

О пользователе: {user_context}
Вопрос: {message}

Отвечай:
- Конкретно и по делу
- С реальными примерами и ресурсами
- На русском языке
- 2-4 абзаца, без воды
"""


async def analyze_career(user_data: dict) -> dict:
    if not openai_client:
        logger.warning("OpenRouter клиент не инициализирован, используются демо-данные")
        return _get_mock_analysis()

    prompt = PROMPT_CAREER_ANALYSIS.format(
        education=user_data.get("education", "не указано"),
        field=user_data.get("field", "не указано"),
        experience=user_data.get("experience", "не указан"),
        interests=", ".join(user_data.get("interests", [])),
        skills=", ".join(user_data.get("skills", [])),
        career_goals=", ".join(user_data.get("career_goals", []))
    )

    try:
        logger.info("Отправляем запрос к OpenRouter AI для анализа карьеры...")
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — AI-карьерный консультант. Отвечай СТРОГО JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        logger.info(f"OpenRouter ответ получен, длина: {len(content)} символов")
        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        logger.info("✅ AI анализ карьеры успешно выполнен")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON парсинг ошибка: {e}")
        return _get_mock_analysis()
    except Exception as e:
        logger.error(f"AI Error при анализе карьеры: {e}")
        return _get_mock_analysis()


async def chat_with_ai(message: str, chat_history: list, user_context: dict = None, extra_context: str = None) -> str:
    if not openai_client:
        logger.warning("OpenRouter клиент не инициализирован, используются демо-данные для чата")
        return _get_mock_chat_response(message)

    try:
        messages = [
            {"role": "system", "content": "Ты — дружелюбный карьерный наставник с глубокими знаниями IT-рынка. Отвечай на русском языке, конкретно и по делу. 2-4 абзаца, без воды."}
        ]

        # Добавляем историю
        for msg in chat_history[-5:]:
            messages.append({"role": "user", "content": msg["user_message"]})
            messages.append({"role": "assistant", "content": msg["ai_response"]})

        # Текущее сообщение с контекстом
        user_msg = f"Вопрос: {message}"
        if user_context:
            user_msg = f"Контекст пользователя: {user_context}\n\nВопрос: {message}"
        
        messages.append({"role": "user", "content": user_msg})

        logger.info(f"AI чат: запрос - {message[:50]}..., сообщений в истории: {len(messages)}")
        
        result = await _call_openai_with_fallback(
            messages=messages,
            temperature=0.8,
            max_tokens=1500
        )
        logger.info("✅ AI чат ответ получен")
        return result
    except Exception as e:
        logger.error(f"AI Error в чате: {e}", exc_info=True)
        return "Извини, возникла ошибка. Попробуй ещё раз!"


async def evaluate_match(user_skills: list, vacancy_requirements: list) -> dict:
    if not openai_client:
        return _get_mock_match(user_skills, vacancy_requirements)

    prompt = f"""
Оцени соответствие пользователя вакансии.

Навыки пользователя: {", ".join(user_skills)}
Требования вакансии: {", ".join(vacancy_requirements)}

Верни СТРОГО JSON:
{{
    "match_score": число 0-100,
    "missing_skills": ["навык 1", "навык 2"],
    "matching_skills": ["навык 1", "навык 2"],
    "recommendations": ["рекомендация 1", "рекомендация 2"]
}}
"""

    try:
        logger.info("AI матчинг: оцениваем соответствие...")
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Отвечай СТРОГО JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )

        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        logger.info("✅ AI матчинг выполнен")
        return result
    except Exception as e:
        logger.error(f"AI Error в матчинге: {e}")
        return _get_mock_match(user_skills, vacancy_requirements)


PROMPT_SKILL_RECOMMENDATIONS = """
Ты — карьерный консульттант. На основе профиля пользователя и его результатов тестирования, дай конкретные рекомендации по развитию навыков.

ПРОФИЛЬ:
- Образование: {education}
- Профессия/направление: {profession}
- Опыт: {experience}
- Навыки: {skills}
- Результаты тестирования: {test_results}

Верни JSON:
{{
    "top_skills_to_develop": [
        {{"skill": "навык", "priority": "высокий|средний|низкий", "why": "зачем нужен", "how_to_learn": "как изучить (конкретные шаги)", "resources": "бесплатные курсы/ресурсы"}}
    ],
    "career_advice": "конкретный совет по развитию карьеры (2-3 предложения)",
    "next_steps": ["шаг 1", "шаг 2", "шаг 3"]
}}

Отвечай конкретно, без общих фраз. Минимум 3 навыка для развития.
"""


async def get_skill_recommendations(user_data: dict, test_results: list) -> dict:
    """Генерирует персональные рекомендации по развитию навыков"""
    if not _openai_client:
        return _get_mock_recommendations(user_data)

    try:
        test_results_str = ", ".join([f"{r.get('role_id', 'unknown')}: {r.get('match_score', 0)}%" for r in test_results]) if test_results else "нет результатов"

        response = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — карьерный консульттант. Даёшь конкретные рекомендации по развитию навыков."},
                {"role": "user", "content": PROMPT_SKILL_RECOMMENDATIONS.format(
                    education=user_data.get('education', 'не указано'),
                    profession=user_data.get('field', user_data.get('profession', 'не указано')),
                    experience=user_data.get('experience', 'нет опыта'),
                    skills=", ".join(user_data.get('skills', [])) or "не указаны",
                    test_results=test_results_str,
                )}
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        import json
        import re
        content = response.choices[0].message.content.strip()
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            return json.loads(json_match.group())
        return _get_mock_recommendations(user_data)

    except Exception as e:
        print(f"Skill recommendations error: {e}")
        return _get_mock_recommendations(user_data)


def _get_mock_recommendations(user_data: dict) -> dict:
    """Моковые рекомендации если AI недоступен"""
    skills = user_data.get('skills', [])
    profession = user_data.get('field', user_data.get('profession', 'специалист'))

    common_skills = ['Коммуникация', 'Английский язык', 'Управление временем', 'Работа в команде']
    missing = [s for s in common_skills if s.lower() not in [sk.lower() for sk in skills]]

    return {
        "top_skills_to_develop": [
            {
                "skill": missing[0] if missing else 'Продвинутые навыки в профессии',
                "priority": "высокий",
                "why": "Критически важно для роста в любой профессии",
                "how_to_learn": "Практикуй каждый день по 30 минут, найди ментора",
                "resources": "YouTube, Stepik, Coursera (бесплатные курсы)"
            },
            {
                "skill": missing[1] if len(missing) > 1 else 'Лидерство',
                "priority": "средний",
                "why": "Поможет расти до senior позиций",
                "how_to_learn": "Возьми ответственность за маленький проект",
                "resources": "Книги: '7 навыков высокоэффективных людей'"
            },
            {
                "skill": missing[2] if len(missing) > 2 else 'Аналитическое мышление',
                "priority": "средний",
                "why": "Нужно для принятия решений на основе данных",
                "how_to_learn": "Решай кейсы, анализируй данные",
                "resources": "Kaggle, бесплатные курсы по аналитике"
            }
        ],
        "career_advice": f"Для роста в направлении '{profession}' фокусируйся на практическом опыте. Делай пет-проекты, участвуй в хакатонах, networking с профессионалами.",
        "next_steps": [
            "Составь план обучения на 3 месяца",
            "Найди ментора в своей области",
            "Пройди тестирование по другим ролям для сравнения"
        ]
    }


PROMPT_QUICK_MATCH = """
Ты — карьерный эксперт.

Пользователь:
- Образование: {education}
- Направление: {field}
- Опыт: {experience}
- Интересы: {interests}
- Навыки: {skills}
- Карьерные цели: {career_goals}

Верни ТОЛЬКО JSON (никакого другого текста):
{{
    "professions": [
        {{"title": "Название профессии", "match_percent": число от 0 до 100, "reason": "почему подходит (1 короткое предложение)"}}
    ]
}}

Минимум 5 профессий.
"""


async def quick_match_career(user_data: dict) -> dict:
    """Матчинг ролей по ответам онбординга — ЧЕСТНЫЙ скоринг"""
    import os, json as _json

    # Наименования ролей
    ROLE_NAMES = {
        "sales_intern": "Менеджер по продажам",
        "hr_intern": "HR-менеджер",
        "ai_analyst": "Аналитик данных / AI",
        "marketing": "Маркетолог",
        "lawyer": "Юрист",
        "procurement": "Специалист по закупкам",
        "engineer_lks": "Инженер телекоммуникаций",
        "seller": "Продавец-консультант",
        "it_support": "IT-поддержка",
        "property_manager": "Менеджер недвижимости",
        "transport": "Логист",
        "corporate_client": "Менеджер по работе с клиентами",
        "admin_support": "Офис-менеджер",
        "python_dev": "Python-разработчик",
        "data_analyst": "Аналитик данных",
        "engineer": "Инженер",
    }

    user_skills = [s.strip().lower() for s in user_data.get("skills", [])]
    user_interests = [i.lower() for i in user_data.get("interests", [])]
    user_field = user_data.get("field", "").lower()

    # Требуемые навыки для каждой роли (на основе HH.ru)
    ROLE_SKILLS = {
        "python_dev": {"python", "sql", "git", "docker", "linux", "fastapi", "postgresql", "rest api"},
        "data_analyst": {"sql", "python", "excel", "pandas", "power bi", "tableau", "анализ данных", "git"},
        "ai_analyst": {"python", "sql", "анализ данных", "power bi", "pandas", "git", "data"},
        "engineer": {"linux", "git", "автоматизация", "сети", "bash", "мониторинг"},
        "engineer_lks": {"linux", "сети", "bash", "автоматизация", "git"},
        "it_support": {"git", "linux", "docker", "windows", "сети"},
        "sales_intern": {"excel", "клиенты", "переговоры", "коммуникация", "crm"},
        "seller": {"клиенты", "коммуникация", "переговоры", "продажи"},
        "corporate_client": {"клиенты", "переговоры", "коммуникация", "crm"},
        "marketing": {"excel", "figma", "коммуникация", "анализ данных", "photoshop", "crm"},
        "hr_intern": {"коммуникация", "excel", "crm"},
        "lawyer": {"excel", "коммуникация", "переговоры", "1с"},
        "procurement": {"excel", "переговоры", "1с", "анализ данных"},
        "property_manager": {"excel", "коммуникация", "figma"},
        "transport": {"excel", "управление", "коммуникация"},
        "admin_support": {"excel", "коммуникация", "управление"},
    }

    # Ключевые слова интересов для каждой роли
    ROLE_INTERESTS = {
        "python_dev": {"разработк", "it и программирование"},
        "data_analyst": {"аналитик", "data", "it и программирование"},
        "ai_analyst": {"искусствен", "интеллект", "ml", "аналитик", "данны"},
        "engineer": {"инженери", "телеком"},
        "engineer_lks": {"инженери", "телеком"},
        "it_support": {"разработк", "it и программирование"},
        "sales_intern": {"продаж", "маркетинг"},
        "seller": {"продаж"},
        "corporate_client": {"продаж", "клиент"},
        "marketing": {"маркетинг", "реклам", "дизайн"},
        "hr_intern": {"hr", "рекрутинг", "подбор"},
        "lawyer": {"юриспруденци", "право"},
        "procurement": {"финанс", "экономик", "закупк"},
        "property_manager": {"дизайн", "креатив", "администрирование"},
        "transport": {"финанс", "администрирование"},
        "admin_support": {"администрирование", "управлен"},
    }

    # Считаем скоринг + matched навыки для каждой роли
    results = {}
    for role_id, required_skills in ROLE_SKILLS.items():
        score = 0
        matched = []

        # 1) Совпадение навыков (0-50 баллов)
        for us in user_skills:
            for rs in required_skills:
                if us == rs or us in rs or rs in us:
                    for orig_s in user_data.get("skills", []):
                        if orig_s.lower() == us:
                            matched.append(orig_s)
                            score += 8
                            break
                    break

        score = min(score, 50)

        # 2) Бонус за поле (0-30)
        field_map = {
            "python_dev": ["it и программирование"],
            "data_analyst": ["аналитика и данные", "it и программирование"],
            "ai_analyst": ["аналитика и данные", "it и программирование"],
            "engineer": ["инженерия и телеком"],
            "engineer_lks": ["инженерия и телеком"],
            "it_support": ["it и программирование"],
            "sales_intern": ["продажи и маркетинг"],
            "seller": ["продажи и маркетинг"],
            "corporate_client": ["продажи и маркетинг"],
            "marketing": ["продажи и маркетинг", "дизайн и креатив"],
            "hr_intern": ["hr и рекрутинг"],
            "lawyer": ["юриспруденция и право"],
            "procurement": ["финансы и экономика"],
            "property_manager": ["дизайн и креатив", "администрирование"],
            "transport": ["финансы и экономика", "администрирование"],
            "admin_support": ["администрирование"],
        }
        for f in field_map.get(role_id, []):
            if f in user_field:
                score += 30
                break

        # 3) Бонус за интересы (0-20)
        if role_id in ROLE_INTERESTS:
            for interest in user_interests:
                for kw in ROLE_INTERESTS[role_id]:
                    if kw in interest:
                        score += 10
                        break
                else:
                    continue
                break

        results[role_id] = {"score": min(score, 95), "matched": matched}

    # Сортируем по score
    sorted_roles = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)

    # Берём только релевантные роли (score >= 15), макс 6
    top_roles = [(rid, data) for rid, data in sorted_roles if data["score"] >= 15][:6]

    # Если ничего релевантного — возвращаем топ-3 по полю
    if not top_roles:
        field_map = {
            "python_dev": ["it и программирование"],
            "data_analyst": ["аналитика и данные", "it и программирование"],
            "ai_analyst": ["аналитика и данные", "it и программирование"],
            "engineer": ["инженерия и телеком"],
            "engineer_lks": ["инженерия и телеком"],
            "it_support": ["it и программирование"],
            "sales_intern": ["продажи и маркетинг"],
            "seller": ["продажи и маркетинг"],
            "corporate_client": ["продажи и маркетинг"],
            "marketing": ["продажи и маркетинг", "дизайн и креатив"],
            "hr_intern": ["hr и рекрутинг"],
            "lawyer": ["юриспруденция и право"],
            "procurement": ["финансы и экономика"],
            "property_manager": ["дизайн и креатив", "администрирование"],
            "transport": ["финансы и экономика", "администрирование"],
            "admin_support": ["администрирование"],
        }
        for field_kw, field_roles in field_map.items():
            if field_kw in user_field:
                for rid in field_roles[:3]:
                    top_roles.append((rid, {"score": 15, "matched": []}))
                break
        if not top_roles:
            top_roles = [("sales_intern", {"score": 15, "matched": []}), ("marketing", {"score": 15, "matched": []}), ("hr_intern", {"score": 15, "matched": []})]

    professions = []
    for role_id, data in top_roles:
        reason = f"Совпадение: {', '.join(data['matched'][:3])}" if data['matched'] else "Может подойти"
        professions.append({
            "title": ROLE_NAMES.get(role_id, role_id),
            "role_id": role_id,
            "match_percent": max(data["score"], 5),
            "reason": reason,
        })

    return {"professions": professions}


async def analyze_scenario_match(role_id: str, user_answers: list) -> dict:
    """AI анализ ответов на сценарии — качественный, с fallback"""
    import json, os

    # Загружаем сценарии из primary
    scenarios_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_primary.json')
    if os.path.exists(scenarios_path):
        with open(scenarios_path, 'r', encoding='utf-8') as f:
            primary_data = json.load(f)
    else:
        primary_data = {"scenarios": []}

    # Загружаем сценарии из HH
    hh_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_from_hh.json')
    if os.path.exists(hh_path):
        with open(hh_path, 'r', encoding='utf-8') as f:
            hh_data = json.load(f)
    else:
        hh_data = {"scenarios": []}

    # Ищем роль в обоих источниках
    role_scenario = None
    for s in primary_data.get("scenarios", []):
        if s.get("role_id") == role_id:
            role_scenario = s
            break
    if not role_scenario:
        for s in hh_data.get("scenarios", []):
            if s.get("role_id") == role_id:
                role_scenario = s
                break

    if not role_scenario:
        return {"match_score": 0, "error": "Role not found"}

    # Если AI недоступен — rule-based fallback
    if not openai_client:
        return _rule_based_scenario_match(user_answers, role_scenario)

    # AI анализ
    questions = role_scenario.get("questions", [])
    answers_text = "\n".join([
        f"Вопрос: {q.get('text', '')}\nОтвет пользователя: {a.get('answer', '')}"
        for q, a in zip(questions, user_answers)
    ])

    prompt = f"""
Ты — эксперт по оценке кандидатов. Проанализируй ответы на тест для роли: {role_scenario.get('role_name', role_id)}.

Вопросы и ответы:
{answers_text}

Оцени качество ответов по шкале 0-100, где:
- 80-100: Отличные ответы, глубокое понимание
- 60-79: Хорошие ответы, базовое понимание с пробелами
- 40-59: Средние ответы, нужно больше подготовки
- 0-39: Слабые ответы, недостаточные знания

Верни СТРОГО JSON:
{{
    "match_score": число 0-100,
    "strengths": ["конкретная сильная сторона 1", "конкретная сильная сторона 2"],
    "weaknesses": ["конкретное слабое место 1", "конкретное слабое место 2"],
    "feedback": "Короткая обратная связь (1-2 предложения, на русском)"
}}
"""
    try:
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — эксперт по оценке кандидатов. Отвечай строго JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=400,
            timeout=30,
        )
        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        result["match_score"] = min(max(result.get("match_score", 0), 0), 100)
        return result
    except Exception as e:
        logger.warning(f"AI scenario analysis failed, using fallback: {e}")
        return _rule_based_scenario_match(user_answers, role_scenario)


def _rule_based_scenario_match(user_answers: list, role_scenario: dict) -> dict:
    """Rule-based fallback для анализа сценариев"""
    questions = role_scenario.get("questions", [])
    if not questions or not user_answers:
        return {"match_score": 0, "error": "No answers"}

    total_score = 0
    total_answered = len(user_answers)

    for answer_data in user_answers:
        answer_text = answer_data.get("answer", "").lower()
        question_id = answer_data.get("question_id", "")

        question = None
        for q in questions:
            if q.get("id") == question_id:
                question = q
                break
        if not question:
            continue

        options = question.get("options", [])
        non_custom = [opt for opt in options if opt != "Свой вариант"]
        best_idx = len(non_custom) - 1

        if answer_text == "свой вариант" or not answer_text:
            total_score += 50
        else:
            answer_idx = -1
            for j, opt in enumerate(options):
                if opt.lower() == answer_text or answer_text in opt.lower()[:30]:
                    answer_idx = j
                    break

            if answer_idx == -1 and best_idx < len(options):
                best_words = set(options[best_idx].lower().split())
                answer_words = set(answer_text.split())
                overlap = len(best_words & answer_words)
                if overlap >= 2:
                    answer_idx = best_idx
                elif overlap >= 1:
                    answer_idx = best_idx - 1
                else:
                    answer_idx = 0

            if answer_idx == best_idx:
                total_score += 100
            elif answer_idx == best_idx - 1:
                total_score += 75
            elif answer_idx == best_idx - 2:
                total_score += 50
            else:
                total_score += 25

    match_score = round(total_score / total_answered) if total_answered > 0 else 0
    pct = match_score / 100

    if pct >= 0.8:
        return {"match_score": match_score, "strengths": ["Отличное понимание роли"], "weaknesses": ["Можно улучшить опыт"], "feedback": "Отлично! Ты хорошо разбираешься."}
    elif pct >= 0.6:
        return {"match_score": match_score, "strengths": ["Базовое понимание"], "weaknesses": ["Нужна практика"], "feedback": "Хороший результат. Есть потенциал."}
    elif pct >= 0.4:
        return {"match_score": match_score, "strengths": ["Есть базовые знания"], "weaknesses": ["Сложные ситуации вызывают трудности"], "feedback": "Средний результат. Стоит подучить."}
    else:
        return {"match_score": match_score, "strengths": ["Желание развиваться"], "weaknesses": ["Недостаточно знаний"], "feedback": "Нужна подготовка. Попробуй через неделю."}


def _get_mock_analysis():
    return {
        "profile_summary": "У тебя хорошая база для старта в IT. Навыки Python и SQL востребованы на рынке, а интерес к программированию — главный драйвер роста.",
        "personality_type": "Python-разработчик с уклоном в данные",
        "strengths": [
            "Python — основной язык для бэкенда и аналитики",
            "SQL — критически важен для работы с данными",
            "Git — основа командной разработки",
            "Аналитическое мышление и готовность учиться"
        ],
        "professions": [
            {
                "title": "Python Developer",
                "match_percent": 88,
                "reason": "Python — твой основной навык. С опытом 1-2 года и знанием SQL ты готов к позициям Junior/Middle разработчика. Рынок растёт, особенно в финтехе и e-commerce.",
                "salary_range": "80 000 - 180 000 ₽"
            },
            {
                "title": "Data Analyst",
                "match_percent": 82,
                "reason": "SQL + Python + интерес к AI/ML — идеальный набор для аналитика данных. Многие компании ищут людей с таким стеком для работы с метриками и отчётами.",
                "salary_range": "70 000 - 150 000 ₽"
            },
            {
                "title": "Backend Developer",
                "match_percent": 75,
                "reason": "Python + Git + SQL позволяют быстро войти в бэкенд. Добавь FastAPI/Django — и ты готов к реальным задачам.",
                "salary_range": "90 000 - 200 000 ₽"
            },
            {
                "title": "ML Engineer (Junior)",
                "match_percent": 65,
                "reason": "Интерес к AI/ML + Python — хорошая стартовая точка. Нужно подтянуть математику и библиотеки ML, но путь понятный.",
                "salary_range": "100 000 - 220 000 ₽"
            },
            {
                "title": "Data Engineer",
                "match_percent": 55,
                "reason": "SQL — база для data engineering. С Python ты сможешь строить пайплайны. Нужно изучить Airflow, Spark, Kafka.",
                "salary_range": "120 000 - 250 000 ₽"
            }
        ],
        "career_path": [
            {
                "step": 1,
                "title": "Углубление в Python",
                "description": "Пройди курс по продвинутому Python: ООП, декораторы, асинхронность, тестирование. Практика: напиши REST API на FastAPI с базой данных и автотестами. Ресурсы: курс 'Поколение Python' на Stepik, книга 'Fluent Python'.",
                "duration": "2-3 месяца"
            },
            {
                "step": 2,
                "title": "Проектное портфолио",
                "description": "Сделай 3 проекта: (1) Telegram-бот с базой данных, (2) REST API с авторизацией и документацией Swagger, (3) Jupyter-ноутбук с анализом датасета из Kaggle. Выложи на GitHub с README.",
                "duration": "2-3 месяца"
            },
            {
                "step": 3,
                "title": "Подготовка к собеседованиям",
                "description": "Решай задачи на LeetCode (50+ Easy/Medium), изучи алгоритмы и структуры данных. Подготовь резюме с описанием проектов. Тренируй поведенческие вопросы (STAR-методика).",
                "duration": "1-2 месяца"
            },
            {
                "step": 4,
                "title": "Поиск работы и нетворкинг",
                "description": "Подавайся на 10+ вакансий в неделю. Участвуй в митапах (Python Moscow, Data Fest). Найди ментора на ADPList. Рассматривай стажировки в Яндексе, Тинькофф, Сбере.",
                "duration": "1-3 месяца"
            }
        ],
        "missing_skills": [
            "FastAPI / Django — фреймворки для веб-разработки",
            "Алгоритмы и структуры данных — для собеседований",
            "Docker — контейнеризация для деплоя",
            "Тестирование (pytest) — обязательно для миддла",
            "CI/CD (GitHub Actions) — автоматизация пайплайна"
        ],
        "recommendations": [
            "Пройди 'Поколение Python' на Stepik (бесплатно) — лучший курс для углубления в Python. После него перейди к FastAPI по документации.",
            "Сделай проект-портфолио: REST API + база данных + Docker. Это покажет работодателю, что ты умеешь работать с реальными технологиями. Выложи на GitHub.",
            "Решай 2-3 задачи LeetCode в неделю. Для Junior достаточно 50 задач Easy/Medium. Это критически важно для прохождения технических собеседований.",
            "Вступи в сообщества: Python Moscow (Telegram), Data Engineering (Telegram), Habr Career. Ходи на митапы — нетворкинг даёт 30% офферов."
        ]
    }


def _get_mock_chat_response(message):
    return "Привет! Рад помочь с карьерой. Расскажи подробнее о твоих навыках и интересах — подберём оптимальный путь."


def _get_mock_match(user_skills, vacancy_requirements):
    user_set = set(s.lower() for s in user_skills)
    req_set = set(s.lower() for s in vacancy_requirements)

    if not req_set:
        return {"match_score": 50, "missing_skills": [], "matching_skills": user_skills[:3], "recommendations": []}

    matching = user_set & req_set
    missing = req_set - user_set
    score = round(len(matching) / len(req_set) * 100) if req_set else 0

    return {
        "match_score": score,
        "missing_skills": list(missing),
        "matching_skills": list(matching),
        "recommendations": [f"Изучи: {skill}" for skill in list(missing)[:3]]
    }


# ============================================================
# НОВЫЕ AI ФУНКЦИИ: Генерация ролей и сценариев
# ============================================================

PROMPT_GENERATE_ROLES = """
Ты — эксперт по карьерному консалтингу с 20-летним опытом. Ты знаешь рынок труда, тренды, зарплатные вилки и требования к каждой роли.

ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:
- Образование: {education}
- Направление/профессия: {profession}
- Опыт: {experience}
- Интересы: {interests}
- Навыки: {skills}
- Цель: {goal}

ЗАДАЧА: Сгенерируй 5-8 ролей, которые подходят ЭТОМУ человеку. Не ограничивайся стандартными — думай креативно, но реалистично.

Верни СТРОГО JSON:
{{
    "roles": [
        {{
            "role_id": "уникальный_id_на_английском",
            "title": "Название роли на русском",
            "match_percent": число 40-95,
            "reason": "Почему подходит (2-3 предложения, ссылайся на конкретные навыки/интересы пользователя)",
            "salary_range": "от X до Y ₽",
            "key_skills": ["навык 1", "навык 2", "навык 3", "навык 4"],
            "growth_path": "Кем можно стать через 2-3 года"
        }}
    ]
}}

ТРЕБОВАНИЯ:
1. role_id — уникальный, на английском, snake_case (например: "python_backend_dev", "data_analyst_ml")
2. title — на русском, конкретная должность
3. match_percent — реалистичный, 40-95
4. reason — персонализированный, НЕ шаблонный
5. key_skills — 4 ключевых навыка для этой роли
6. growth_path — конкретная перспектива роста
7. Реальные зарплаты для России 2025
8. Минимум 5 ролей, максимум 8

Ответ ТОЛЬКО JSON.
"""


async def generate_roles_for_profile(user_data: dict) -> dict:
    """AI генерирует динамический список ролей на основе профиля пользователя.
    Использует БЫСТРУЮ модель — ответ за 2-5 сек."""
    if not openai_client:
        logger.warning("OpenRouter клиент не инициализирован, используются демо-роли")
        return _get_mock_generated_roles(user_data)

    prompt = PROMPT_GENERATE_ROLES.format(
        education=user_data.get("education", "не указано"),
        profession=user_data.get("field", user_data.get("profession", "не указано")),
        experience=user_data.get("experience", "не указан"),
        interests=", ".join(user_data.get("interests", [])) or "не указаны",
        skills=", ".join(user_data.get("skills", [])) or "не указаны",
        goal=", ".join(user_data.get("career_goals", [])) or "не указана",
    )

    try:
        logger.info(f"⚡ Быстрая генерация ролей (FAST_MODEL: {FAST_MODEL}) для профиля ({user_data.get('field', 'unknown')})")
        response = await openai_client.chat.completions.create(
            model=FAST_MODEL,
            messages=[
                {"role": "system", "content": "Ты — карьерный эксперт. Отвечай СТРОГО JSON. Никакого текста кроме JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            timeout=15
        )
        content = response.choices[0].message.content.strip()
        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        logger.info(f"✅ AI сгенерировал {len(result.get('roles', []))} ролей (быстрая модель)")
        return result
    except Exception as e:
        logger.warning(f"Fast model failed for roles: {e}, trying quality model...")
        # Fallback на quality модель
        try:
            response = await openai_client.chat.completions.create(
                model=QUALITY_MODEL,
                messages=[
                    {"role": "system", "content": "Ты — карьерный эксперт. Отвечай СТРОГО JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000,
                timeout=30
            )
            content = response.choices[0].message.content.strip()
            content = content.strip().strip("```json").strip("```").strip()
            result = json.loads(content)
            logger.info(f"✅ AI сгенерировал {len(result.get('roles', []))} ролей (quality модель)")
            return result
        except Exception as e2:
            logger.error(f"All models failed for roles: {e2}")
            return _get_mock_generated_roles(user_data)


PROMPT_GENERATE_SCENARIO = """
Ты — эксперт по оценке кандидатов для роли: {role_title}.

РОЛЬ: {role_title}
ОПИСАНИЕ: {role_reason}
КЛЮЧЕВЫЕ НАВЫКИ: {key_skills}

ПРОФИЛЬ КАНДИДАТА:
- Образование: {education}
- Опыт: {experience}
- Навыки: {user_skills}

ЗАДАЧА: Создай ситуационный тест из 3-5 вопросов, которые проверят, насколько кандидат подходит для этой роли.

Каждый вопрос — реальная рабочая ситуация, с которой сталкивается {role_title}.
Варианты ответов должны отражать РАЗНЫЙ уровень компетенции (от новичка до эксперта).

Верни СТРОГО JSON:
{{
    "role_id": "{role_id}",
    "role_name": "{role_title}",
    "questions": [
        {{
            "id": "{role_id}_q1",
            "text": "Текст ситуационного вопроса",
            "options": [
                "Вариант ответа 1 (уровень новичка)",
                "Вариант ответа 2 (базовое понимание)",
                "Вариант ответа 3 (хорошее понимание)",
                "Вариант ответа 4 (экспертный уровень)",
                "Свой вариант"
            ]
        }}
    ]
}}

ТРЕБОВАНИЯ:
1. Ровно 3-5 вопросов (не больше, не меньше)
2. Каждый вопрос — РЕАЛЬНАЯ ситуация на работе
3. 5 вариантов ответов (4 готовых + "Свой вариант")
4. Варианты от слабого к сильному (последний = лучший)
5. Вопросы релевантны именно этой роли
6. Адаптируй сложность под опыт кандидата

Ответ ТОЛЬКО JSON.
"""


async def generate_scenario_for_role(role_data: dict, user_data: dict) -> dict:
    """AI генерирует ситуационный тест для конкретной роли.
    Использует КАЧЕСТВЕННУЮ модель — ответ за 5-15 сек."""
    if not openai_client:
        logger.warning("OpenRouter клиент не инициализирован, демо-сценарий")
        return _get_mock_scenario(role_data)

    prompt = PROMPT_GENERATE_SCENARIO.format(
        role_title=role_data.get("title", "Специалист"),
        role_id=role_data.get("role_id", "unknown"),
        role_reason=role_data.get("reason", ""),
        key_skills=", ".join(role_data.get("key_skills", [])),
        education=user_data.get("education", "не указано"),
        experience=user_data.get("experience", "не указан"),
        user_skills=", ".join(user_data.get("skills", [])) or "не указаны",
    )

    try:
        logger.info(f"🧠 Генерация сценария (QUALITY_MODEL) для {role_data.get('title', 'unknown')}")
        response = await openai_client.chat.completions.create(
            model=QUALITY_MODEL,
            messages=[
                {"role": "system", "content": "Ты — эксперт по оценке кандидатов. Отвечай СТРОГО JSON. Никакого текста кроме JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000,
            timeout=30
        )
        content = response.choices[0].message.content.strip()
        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        question_count = len(result.get("questions", []))
        logger.info(f"✅ AI сгенерировал сценарий: {question_count} вопросов для {role_data.get('title', 'unknown')}")
        return result
    except Exception as e:
        logger.warning(f"Quality model failed for scenario: {e}, trying fast model...")
        # Fallback на быструю модель
        try:
            response = await openai_client.chat.completions.create(
                model=FAST_MODEL,
                messages=[
                    {"role": "system", "content": "Ты — эксперт по оценке кандидатов. Отвечай СТРОГО JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                timeout=15
            )
            content = response.choices[0].message.content.strip()
            content = content.strip().strip("```json").strip("```").strip()
            result = json.loads(content)
            question_count = len(result.get("questions", []))
            logger.info(f"✅ AI сгенерировал сценарий: {question_count} вопросов (fast модель)")
            return result
        except Exception as e2:
            logger.error(f"All models failed for scenario: {e2}")
            return _get_mock_scenario(role_data)


def _get_mock_generated_roles(user_data: dict) -> dict:
    """Демо-роли если AI недоступен"""
    profession = user_data.get("field", user_data.get("profession", "специалист"))
    skills = user_data.get("skills", [])

    return {
        "roles": [
            {
                "role_id": "junior_special",
                "title": f"Junior {profession}",
                "match_percent": 65,
                "reason": f"Твои навыки ({', '.join(skills[:3]) if skills else 'базовые'}) — хорошая стартовая позиция. Нужно подтянуть практический опыт.",
                "salary_range": "40 000 - 70 000 ₽",
                "key_skills": ["Базовые знания профессии", "Готовность учиться", "Работа в команде"],
                "growth_path": "Middle → Senior → Team Lead"
            },
            {
                "role_id": "analyst_entry",
                "title": "Аналитик данных (Junior)",
                "match_percent": 55,
                "reason": "Аналитика — растущее направление. С базовыми навыками можно начать с позиции Junior-аналитика.",
                "salary_range": "50 000 - 80 000 ₽",
                "key_skills": ["Excel", "SQL", "Аналитическое мышление", "Визуализация данных"],
                "growth_path": "Middle Analyst → Senior → Data Scientist"
            },
            {
                "role_id": "project_coord",
                "title": "Координатор проектов",
                "match_percent": 50,
                "reason": "Хороший вход в управление проектами. Подходит для людей с организованностью и коммуникативными навыками.",
                "salary_range": "45 000 - 75 000 ₽",
                "key_skills": ["Управление задача", "Коммуникация", "Документация", "Agile"],
                "growth_path": "Project Manager → Program Manager → Director"
            }
        ]
    }


def _get_mock_scenario(role_data: dict) -> dict:
    """Демо-сценарий если AI недоступен"""
    role_id = role_data.get("role_id", "demo")
    role_name = role_data.get("title", "Специалист")

    return {
        "role_id": role_id,
        "role_name": role_name,
        "questions": [
            {
                "id": f"{role_id}_q1",
                "text": f"Тебе поручили задачу, с которой ты раньше не сталкивался. Как поступишь?",
                "options": [
                    "Скажу, что не умею и попрошу другую задачу",
                    "Погуглю и попробую разобраться сам",
                    "Изучу документацию, попробую, потом спрошу у коллег",
                    "Составлю план изучения, оценю сроки, сообщу руководителю о рисках",
                    "Свой вариант"
                ]
            },
            {
                "id": f"{role_id}_q2",
                "text": f"Как ты расставляешь приоритеты в работе?",
                "options": [
                    "Делаю то, что проще",
                    "Делаю то, что скажет начальник",
                    "Оцениваю сроки и важность, составляю план",
                    "Использую матрицу Эйзенхауэра, синхронизирую с командой и стейкхолдерами",
                    "Свой вариант"
                ]
            },
            {
                "id": f"{role_id}_q3",
                "text": f"Коллега просит помочь, но у тебя дедлайн. Что сделаешь?",
                "options": [
                    "Брошу всё и помогу",
                    "Откажу, у меня дедлайн",
                    "Помогу после дедлайна или подскажу ресурсы",
                    "Оценю срочность коллеги, делегирую или найду компромисс",
                    "Свой вариант"
                ]
            }
        ]
    }

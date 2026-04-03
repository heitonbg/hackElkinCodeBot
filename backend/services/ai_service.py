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
Ты — ведущий IT-карьерный консультант МТС с 15-летним опытом найма. Ты знаешь рынок изнутри и понимаешь, какие навыки нужны для каждой роли.

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

PROMPT_QUICK_MATCH = """
Ты — карьерный эксперт МТС.

Пользователь:
- Образование: {education}
- Направление: {field}
- Опыт: {experience}
- Навыки: {skills}

Верни ТОЛЬКО JSON с 5 профессиями:
{{
    "professions": [
        {{"title": "Название", "match_percent": число, "reason": "почему подходит (1 предложение)"}}
    ]
}}

Ничего лишнего. Только JSON.
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

async def quick_match_career(user_data: dict) -> dict:
    """Быстрый AI матчинг — только профессии с %"""
    if not openai_client:
        # Демо-режим (без AI)
        return {
            "professions": [
                {"title": "Стажёр продаж", "match_percent": 85, "reason": "Отличная коммуникация и работа с людьми"},
                {"title": "Стажёр HR", "match_percent": 78, "reason": "Интерес к рекрутингу и работе с кандидатами"},
                {"title": "Маркетолог", "match_percent": 72, "reason": "Креативное мышление и аналитика"},
                {"title": "Аналитик данных", "match_percent": 68, "reason": "Навыки Excel и аналитический склад ума"},
                {"title": "IT-стажёр", "match_percent": 65, "reason": "Технические навыки и интерес к IT"},
                {"title": "Специалист закупок", "match_percent": 55, "reason": "Внимательность к деталям и документам"}
            ]
        }
    
    prompt = f"""
Ты — карьерный эксперт МТС.

Пользователь:
- Образование: {user_data.get('education', 'не указано')}
- Направление: {user_data.get('field', 'не указано')}
- Опыт: {user_data.get('experience', 'не указан')}
- Навыки: {', '.join(user_data.get('skills', []))}

Верни ТОЛЬКО JSON (никакого другого текста):
{{
    "professions": [
        {{"title": "Название профессии", "match_percent": число от 0 до 100, "reason": "почему подходит (1 короткое предложение)"}}
    ]
}}

Минимум 5 профессий из списка МТС: продажи, HR, маркетинг, аналитика, IT, юрист, закупки, инженерия.
"""
    try:
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Отвечай строго JSON. Никаких пояснений."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        content = content.strip().strip("```json").strip("```").strip()
        result = json.loads(content)
        return result
    except Exception as e:
        logger.error(f"Quick match error: {e}")
        return {
            "professions": [
                {"title": "Стажёр продаж", "match_percent": 85, "reason": "Коммуникабельность"},
                {"title": "Стажёр HR", "match_percent": 78, "reason": "Работа с людьми"},
                {"title": "Маркетинг", "match_percent": 72, "reason": "Креативность"},
                {"title": "Аналитик данных", "match_percent": 68, "reason": "Аналитика"},
                {"title": "IT-стажёр", "match_percent": 65, "reason": "Технический интерес"}
            ]
        }


async def chat_with_ai(message: str, chat_history: list, user_context: dict = None, extra_context: str = None) -> str:
    if not openai_client:
        logger.warning("OpenRouter клиент не инициализирован, используются демо-данные для чата")
        return _get_mock_chat_response(message)

    try:
        messages = [
            {"role": "system", "content": "Ты — дружелюбный карьерный наставник МТС с глубокими знаниями IT-рынка. Отвечай на русском языке, конкретно и по делу. 2-4 абзаца, без воды."}
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

async def analyze_scenario_match(role_id: str, user_answers: list) -> dict:
    """
    Анализирует ответы пользователя на сценарии и возвращает процент совпадения с ролью
    """
    # Загружаем сценарии
    import json, os
    scenarios_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_primary.json')
    
    with open(scenarios_path, 'r', encoding='utf-8') as f:
        scenarios_data = json.load(f)
    
    # Находим нужную роль
    role_scenario = None
    for s in scenarios_data.get("scenarios", []):
        if s.get("role_id") == role_id:
            role_scenario = s
            break
    
    if not role_scenario:
        return {"match_score": 0, "error": "Role not found"}
    
    # Загружаем требования к роли из mts_vacancies
    from services.mts_vacancies import get_vacancy_by_id
    vacancy = get_vacancy_by_id(role_id)
    requirements = vacancy.get("requirements", []) if vacancy else []
    
    if not openai_client:
        # Демо-режим: считаем через простую логику
        return _simple_scenario_match(user_answers, requirements, role_scenario)
    
    # Режим с AI
    prompt = f"""
Ты — эксперт по подбору персонала МТС.

Роль: {role_scenario.get('role_name')}

Требования к роли:
{chr(10).join(['- ' + r for r in requirements])}

Вопросы и ответы пользователя:
{chr(10).join([f"Вопрос: {q}\nОтвет: {a.get('answer', '')}" for q, a in zip(role_scenario.get('questions', []), user_answers)])}

Оцени, насколько ответы пользователя соответствуют требованиям роли.
Верни ТОЛЬКО JSON:
{{
    "match_score": число 0-100,
    "strengths": ["сильная сторона 1", "сильная сторона 2"],
    "weaknesses": ["слабое место 1", "слабое место 2"],
    "feedback": "короткая обратная связь (1-2 предложения)"
}}
"""
    try:
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — эксперт по оценке кандидатов. Отвечай строго JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        content = content.strip().strip("```json").strip("```").strip()
        return json.loads(content)
    except Exception as e:
        logger.error(f"Scenario analysis error: {e}")
        return _simple_scenario_match(user_answers, requirements, role_scenario)


def _simple_scenario_match(user_answers: list, requirements: list, role_scenario: dict) -> dict:
    """Простой матчинг без AI (для демо)"""
    # Собираем все ответы в одну строку
    answers_text = " ".join([a.get("answer", "").lower() for a in user_answers])
    
    # Считаем, сколько требований задето
    matched = 0
    for req in requirements:
        req_lower = req.lower()
        # Ищем ключевые слова из требования в ответах
        keywords = req_lower.split()[:3]  # первые 3 слова
        if any(kw in answers_text for kw in keywords):
            matched += 1
    
    match_score = round(matched / len(requirements) * 100) if requirements else 50
    
    return {
        "match_score": match_score,
        "strengths": ["Хорошая коммуникация" if "говор" in answers_text else "Базовые знания"],
        "weaknesses": ["Требуется практика" if match_score < 70 else "—"],
        "feedback": f"Ты набрал {match_score}% соответствия. " + ("Отличный результат!" if match_score > 70 else "Есть куда расти!")
    }

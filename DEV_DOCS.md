# 📘 AI Career Navigator МТС — Полная документация разработчика

> Версия: 2.0 (с диагностикой)
> Последнее обновление: Апрель 2026

---

## 📋 Содержание

1. [Обзор проекта](#1-обзор-проекта)
2. [Архитектура системы](#2-архитектура-системы)
3. [Структура проекта](#3-структура-проекта)
4. [Стек технологий](#4-стек-технологий)
5. [База данных](#5-база-данных)
6. [Backend API](#6-backend-api)
7. [Frontend](#7-frontend)
8. [Сервисы](#8-сервисы)
9. [Диагностический тест](#9-диагностический-тест)
10. [Scenario Runner](#10-scenario-runner)
11. [Данные](#11-данные)
12. [Настройка окружения](#12-настройка-окружения)
13. [Запуск проекта](#13-запуск-проекта)
14. [Пользовательские потоки](#14-пользовательские-потоки)
15. [Деплой](#15-деплой)
16. [FAQ и частые проблемы](#16-faq-и-частые-проблемы)

---

## 1. Обзор проекта

**AI Career Navigator** — это интеллектуальный карьерный навигатор для компании МТС, реализованный в формате **Telegram Mini App**.

### Основная идея

Пользователь проходит короткий диагностический тест (10 вопросов), получает персональные рекомендации профессий из 197 доступных, выбирает подходящие роли и проходит интерактивные сценарии-тесты. По результатам — мгновенный скоринг + AI-анализ с рекомендациями по развитию.

### Ключевые возможности

| Функция | Описание |
|---|---|
| 🔍 **Диагностика** | 10 вопросов → определение подходящих категорий и ролей |
| 💼 **197 ролей** | База ролей в 30 категориях с навыками, зарплатами, сценариями |
| 🎮 **Сценарии** | Интерактивные тесты с мгновенным rule-based скорингом |
| 🤖 **AI-анализ** | Фоновый анализ результатов через OpenRouter (Qwen/Step) |
| 💼 **Вакансии HH.ru** | Поиск реальных вакансий по профессии и городу |
| 💬 **AI-чат** | Персональный карьерный наставник |
| 📊 **Лидерборд** | Рейтинг пользователей по результатам тестов |
| 🔄 **Перетест** | Повторное тестирование с кулдауном 7 дней |

### Целевая аудитория

- Студенты, ищущие первую профессию
- Начинающие специалисты, меняющие направление
- Сотрудники МТС, планирующие карьерный рост

---

## 2. Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                      Telegram Mini App                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │◄──►│  React +     │◄──►│ Vite Dev     │  │
│  │   (SPA)      │    │  Vite        │    │ Server :5173 │  │
│  └──────┬───────┘    └──────────────┘    └──────────────┘  │
│         │                                                    │
│         │ HTTP/JSON                                          │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │◄──►│  FastAPI     │◄──►│ Uvicorn      │  │
│  │   API        │    │  :8000       │    │ Server       │  │
│  └─────────────┘    ──────────────┘    ──────────────┘  │
│         │                                                    │
│    ┌────┴────┬────────────┬──────────┐                     │
│    ▼         ▼            ▼          ▼                     │
│ ┌────── ┌────── ┌────────── ┌──────────┐               │
│ │SQLite│ │Open- │ │ HH.ru    │ │ Telegram │               │
│ │  DB  │ │Router│ │ API      │ │ Bot API  │               │
│ └────── └──────┘ ──────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Структура проекта

```
c:\vscode\elkincode\
├── .env                          # Секретные ключи (не коммитить!)
├── .env.example                  # Шаблон для .env
├── .gitignore
├── requirements.txt              # Python зависимости
├── DEV_DOCS.md                   # Этот файл
│
├── backend/                      # FastAPI сервер
│   ├── main.py                   # Точка входа, роуты, CORS, startup
│   ├── database/
│   │   └── db.py                 # SQLite async (9 таблиц)
│   ├── models/
│   │   └── models.py             # Pydantic модели
│   ├── api/                      # API роутеры
│   │   ├── __init__.py
│   │   ├── user.py               # Профиль, онбординг, статистика
│   │   ├── career.py             # AI анализ карьеры
│   │   ├── chat.py               # AI чат-наставник
│   │   ├── vacancies.py          # HH.ru вакансии
│   │   ├── scenarios.py          # Сценарии, лидерборд, перетест
│   │   ├── roles.py              # Быстрый rule-based матчинг
│   │   └── onboarding.py         # Диагностика (НОВЫЙ)
│   ├── services/                 # Бизнес-логика
│   │   ├── ai_service.py         # OpenRouter AI
│   │   ├── hh_service.py         # HH.ru API клиент
│   │   ├── matching_service.py   # AI матчинг вакансий
│   │   ├── mts_vacancies.py      # Вакансии МТС (13 штук)
│   │   ├── mts_matching.py       # Матчинг с вакансиями МТС
│   │   ├── role_matcher.py       # Rule-based матчинг ролей
│   │   ├── diagnostic_scorer.py  # Диагностический скоринг (НОВЫЙ)
│   │   ├── scenario_scorer.py    # Скоринг сценариев
│   │   ├── async_analyzer.py     # Фоновый AI-анализ
│   │   └── scenario_hh_generator.py
│   ├── scripts/
│   │   ├── roles_data.py
│   │   └── generate_roles_db.py
│   └── data/                     # Статические данные
│       ├── roles_database.json       # 197 ролей
│       ├── diagnostic_questions.json # 10 вопросов (НОВЫЙ)
│       ├── scenarios_primary.json
│       ├── scenarios_from_hh.json
│       └── hh_requirements.json
│
├── frontend/                     # React SPA
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx              # Точка входа
│       ├── App.jsx               # Роутинг
│       ├── index.css             # Стили (МТС дизайн)
│       ├── api/
│       │   └── client.js         # API клиент
│       ├── components/
│       │   └── BottomNav.jsx     # Нижняя навигация
│       └── pages/
│           ├── Onboarding.jsx
│           ├── QuickOnboarding.jsx
│           ├── DiagnosticTest.jsx    # (НОВЫЙ)
│           ├── RoleSelection.jsx
│           ├── ScenarioRunner.jsx
│           ├── Dashboard.jsx
│           ├── CareerPath.jsx
│           ├── Vacancies.jsx
│           └── Chat.jsx
│
└── bot/
    └── bot.py                    # Telegram бот
```

---

## 4. Стек технологий

### Backend

| Технология | Версия | Назначение |
|---|---|---|
| **Python** | 3.10+ | Язык |
| **FastAPI** | 0.115+ | REST API фреймворк |
| **Uvicorn** | 0.30+ | ASGI сервер |
| **AsyncOpenAI** | 1.50+ | OpenRouter AI клиент |
| **HTTPX** | 0.27+ | Асинхронные HTTP запросы |
| **AioSQLite** | 0.20+ | Async SQLite |
| **Pydantic** | 2.10+ | Валидация данных |
| **python-dotenv** | 1.0+ | Загрузка .env |
| **python-telegram-bot** | 21.6+ | Telegram бот |

### Frontend

| Технология | Версия | Назначение |
|---|---|---|
| **React** | 18+ | UI фреймворк |
| **Vite** | 5+ | Сборщик + dev сервер |
| **react-router-dom** | 6+ | Клиентский роутинг |
| **Telegram WebApp SDK** | 7.0+ | Интеграция с Telegram |

### Внешние API

| Сервис | Назначение |
|---|---|
| **OpenRouter** | AI модели: qwen/qwen3.6-plus, stepfun/step-3.5-flash |
| **HH.ru API** | Поиск вакансий, справочник городов |
| **Telegram Bot API** | Запуск Mini App |

---

## 5. База данных

**Движок:** SQLite (async через `aiosqlite`)
**Файл:** `career_navigator.db` (создаётся автоматически)

### Таблицы (9 штук)

#### users
Профиль пользователя.

| Поле | Тип | Описание |
|---|---|---|
| `telegram_id` | TEXT PK | ID пользователя Telegram |
| `education` | TEXT | Образование |
| `field` | TEXT | Поле/профессия |
| `experience` | TEXT | Опыт работы |
| `interests` | TEXT (JSON) | Интересы (массив) |
| `skills` | TEXT (JSON) | Навыки (массив) |
| `career_goals` | TEXT (JSON) | Карьерные цели (массив) |
| `created_at` | TIMESTAMP | Дата создания |
| `updated_at` | TIMESTAMP | Дата обновления |

#### career_analyses
Результаты AI-анализа карьеры.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `full_analysis` | TEXT (JSON) | Полный анализ |
| `created_at` | TIMESTAMP | |

#### vacancy_matches
Матчинг вакансий.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `vacancy_id` | TEXT | ID вакансии |
| `profession` | TEXT | Профессия |
| `match_score` | INTEGER | Процент совпадения |
| `missing_skills` | TEXT (JSON) | Недостающие навыки |
| `recommendations` | TEXT (JSON) | Рекомендации |

#### chat_history
История чата.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `user_message` | TEXT | Сообщение пользователя |
| `ai_response` | TEXT | Ответ AI |
| `context` | TEXT | Контекст |
| `created_at` | TIMESTAMP | |

#### scenario_results
Результаты прохождения сценариев.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `role_id` | TEXT | ID роли |
| `match_score` | INTEGER | Процент совпадения |
| `strengths` | TEXT (JSON) | Сильные стороны |
| `weaknesses` | TEXT (JSON) | Зоны роста |
| `feedback` | TEXT | Обратная связь |
| `created_at` | TIMESTAMP | |

#### retest_cooldowns
Кулдаун перетеста (7 дней).

| Поле | Тип | Описание |
|---|---|---|
| `telegram_id` | TEXT PK | |
| `last_test_date` | TIMESTAMP | Дата последнего теста |
| `next_available_date` | TIMESTAMP | Дата следующего доступного теста |

#### scenario_answers
Сырые ответы на сценарии.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `role_id` | TEXT | ID роли |
| `answers` | TEXT (JSON) | Ответы |
| `analyzed` | BOOLEAN | Обработан ли AI |
| `created_at` | TIMESTAMP | |

#### generated_scenarios
AI-сгенерированные сценарии (кэш).

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `role_id` | TEXT | ID роли |
| `scenario_json` | TEXT (JSON) | Сценарий |
| `created_at` | TIMESTAMP | |

#### ai_analyses
AI-анализы результатов сценариев.

| Поле | Тип | Описание |
|---|---|---|
| `id` | INTEGER PK | |
| `telegram_id` | TEXT FK → users | |
| `role_id` | TEXT | ID роли |
| `analysis_json` | TEXT (JSON) | AI-анализ |
| `created_at` | TIMESTAMP | |

---

## 6. Backend API

### Health Check

```
GET /api/health
```
**Response:**
```json
{"status": "ok", "service": "AI Career Navigator"}
```

---

### User (`/api/user/*`)

```
POST /api/user/onboarding
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "education": "Бакалавриат",
  "field": "IT и программирование",
  "experience": "Нет опыта",
  "interests": ["программирование", "дизайн"],
  "skills": ["Python", "React"],
  "career_goals": ["стать разработчиком"]
}
```
**Response:** `{"status": "success", "message": "Данные сохранены"}`

---

```
GET /api/user/profile/{telegram_id}
```
**Response:**
```json
{
  "exists": true,
  "profile": {
    "telegram_id": "123456789",
    "education": "Бакалавриат",
    "field": "IT и программирование",
    "experience": "Нет опыта",
    "interests": ["программирование"],
    "skills": ["Python"],
    "career_goals": [],
    "created_at": "2026-04-04T12:00:00",
    "updated_at": "2026-04-04T12:00:00"
  }
}
```

---

```
GET /api/user/stats/{telegram_id}
```
**Response:**
```json
{
  "exists": true,
  "skills_count": 3,
  "interests_count": 2,
  "goals_count": 1,
  "has_analysis": true,
  "profile_complete": 60
}
```

---

### Career (`/api/career/*`)

```
POST /api/career/analyze
```
**Request:** `{"telegram_id": "123456789"}`

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "professions": ["Python-разработчик", "Data Analyst"],
    "career_path": ["Junior → Middle → Senior"],
    "missing_skills": ["Docker", "PostgreSQL"],
    "recommendations": ["Изучи Docker", "Пройди курс по SQL"]
  }
}
```

---

```
GET /api/career/result/{telegram_id}
GET /api/career/quick-match
GET /api/career/recommendations/{telegram_id}
GET /api/career/generate-roles
GET /api/career/generate-scenario
```

---

### Chat (`/api/chat/*`)

```
POST /api/chat/message
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "message": "Какие навыки нужны для Python-разработчика?",
  "context": "Python-разработчик"
}
```
**Response:** `{"response": "Для Python-разработчика нужны..."}`

---

```
GET /api/chat/history/{telegram_id}?limit=20
```

---

### Vacancies (`/api/vacancies/*`)

```
GET /api/vacancies/search?profession=Python&location=Москва&limit=20
```
**Response:**
```json
{
  "vacancies": [...],
  "count": 15,
  "source": "hh.ru"
}
```

---

```
POST /api/vacancies/match
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "profession": "Python-разработчик",
  "location": "Москва"
}
```

---

### Scenarios (`/api/scenarios/*`)

```
GET /api/scenarios/scenarios
GET /api/scenarios/scenarios/hh
GET /api/scenarios/scenarios/{role_id}
GET /api/scenarios/all-roles
GET /api/scenarios/my-scenarios/{telegram_id}
GET /api/scenarios/leaderboard?limit=20
GET /api/scenarios/retest-status/{telegram_id}
POST /api/scenarios/retest-start/{telegram_id}
POST /api/scenarios/retest-complete/{telegram_id}
POST /api/scenarios/scenarios/save-answers
POST /api/scenarios/scenarios/analyze
POST /api/scenarios/scenarios/analyze-pending/{telegram_id}
GET /api/scenarios/scenarios/pending-count/{telegram_id}
```

---

### Roles (`/api/roles/*`) — быстрый rule-based матчинг

```
POST /api/roles/match
```
**Request:** `{"telegram_id": "123456789"}`

**Response:**
```json
{
  "roles": [
    {
      "role_id": "python_dev",
      "title": "Python-разработчик",
      "category": "IT и разработка",
      "category_emoji": "💻",
      "match_percent": 85,
      "reason": "Навыки: Python, SQL; Совпадение по направлению",
      "skills": ["Python", "SQL", "Git", "Docker"],
      "salary": {"junior": "60-90k ₽", "middle": "120-200k ₽"},
      "scenarios_available": ["junior", "middle"]
    }
  ],
  "count": 12
}
```

---

```
GET /api/roles/all
GET /api/roles/search?q=python
GET /api/roles/scenario/{role_id}?level=junior
```

---

```
POST /api/roles/score
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "role_id": "python_dev",
  "level": "junior",
  "answers": [
    {"question_id": "q1", "answer": "REST API — это архитектурный стиль"},
    {"question_id": "q2", "answer": "Посмотрю логи"}
  ]
}
```
**Response:** (мгновенный, rule-based)
```json
{
  "match_score": 75,
  "level": "junior",
  "level_label": "Хороший",
  "details": [...],
  "feedback": "Вы хорошо разбираетесь в..."
}
```
*(Фоновый AI-анализ запускается автоматически)*

---

```
GET /api/roles/ai-analysis/{telegram_id}?role_id=python_dev
```
**Response:**
```json
{
  "status": "completed",
  "analysis": {
    "strengths": ["Знание REST API", "Умение работать с логами"],
    "weaknesses": ["Git ветвление"],
    "recommendations": ["Изучи Git Flow"],
    "next_role_suggestion": "backend_dev"
  }
}
```
или `{"status": "pending"}` (если AI ещё анализирует)

---

### Onboarding/Diagnostic (`/api/onboarding/*`) — НОВЫЙ

```
GET /api/onboarding/questions
```
**Response:**
```json
{
  "questions": [
    {
      "id": "q1",
      "text": "Что тебе ближе всего?",
      "options": [
        {
          "text": "Создавать что-то новое с нуля",
          "scores": {"it_and_development": 8, "design_and_creative": 10}
        }
      ]
    }
  ],
  "count": 10
}
```

---

```
POST /api/onboarding/diagnostic
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "answers": [
    {"question_id": "q1", "answer": "Создавать что-то новое с нуля"},
    {"question_id": "q2", "answer": "В одиночку, в тишине и концентрации"}
  ]
}
```
**Response:**
```json
{
  "top_categories": [
    {"category_id": "it_and_development", "category_name": "IT и разработка", "score": 73},
    {"category_id": "design_and_creative", "category_name": "Дизайн и креатив", "score": 54}
  ],
  "recommended_roles": [
    {
      "role_id": "python_dev",
      "title": "Python-разработчик",
      "category": "IT и разработка",
      "category_emoji": "💻",
      "match_percent": 73,
      "reason": "Подходит по направлению: IT и разработка"
    }
  ],
  "total_questions": 10,
  "answered_questions": 10
}
```

---

```
POST /api/onboarding/save-profile
```
**Request:**
```json
{
  "telegram_id": "123456789",
  "education": "Бакалавриат",
  "field": "IT и разработка",
  "experience": "Нет опыта",
  "interests": [],
  "skills": [],
  "career_goals": []
}
```

---

## 7. Frontend

### Роутинг (`App.jsx`)

| Путь | Компонент | Описание |
|---|---|---|
| `/` | → `/diagnostic` | Редирект |
| `/diagnostic` | `DiagnosticTest` | 10-вопросный тест |
| `/onboarding` | `Onboarding` | 3-шаговый онбординг |
| `/role-selection` | `RoleSelection` | Выбор ролей |
| `/scenario-runner` | `ScenarioRunner` | Прохождение тестов |
| `/career` | `CareerPath` + `BottomNav` | Выбор ролей + результаты |
| `/dashboard` | `Dashboard` + `BottomNav` | Профиль + результаты |
| `/vacancies` | `Vacancies` + `BottomNav` | Поиск вакансий HH |
| `/chat` | `Chat` + `BottomNav` | AI чат |
| `/*` | → `/career` | Catch-all |

### BottomNav

4 вкладки: 🚀 Карьера, 👤 Профиль, 💼 Вакансии, 💬 Чат

### API клиент (`api/client.js`)

```javascript
import { api } from '../api/client'

// Пример использования
const questions = await api.getDiagnosticQuestions()
const results = await api.runDiagnostic(answers)
const roles = await api.matchRoles()
const scenario = await api.getScenario('python_dev', 'junior')
const score = await api.scoreScenario('python_dev', 'junior', answers)
```

Все методы:

| Метод | Endpoint |
|---|---|
| `getDiagnosticQuestions()` | GET /onboarding/questions |
| `runDiagnostic(answers)` | POST /onboarding/diagnostic |
| `saveProfile(data)` | POST /onboarding/save-profile |
| `matchRoles()` | POST /roles/match |
| `getAllRoles()` | GET /roles/all |
| `searchRoles(q)` | GET /roles/search?q= |
| `getScenario(roleId, level)` | GET /roles/scenario/{id}?level= |
| `scoreScenario(roleId, level, answers)` | POST /roles/score |
| `getAiAnalysis(roleId)` | GET /roles/ai-analysis/{id} |

---

## 8. Сервисы

### `role_matcher.py` — Rule-based матчинг ролей

**Алгоритм (0-100 баллов):**
1. Навыки пользователя vs required_skills роли (0-30)
2. Поле/образование vs category роли (0-30)
3. Интересы vs keywords категории (0-20)
4. Опыт работы (0-20)

**Порог:** min 10 баллов. Если 0 ролей — fallback на 8 популярных ролей.

**Файл эмодзи:** `CATEGORY_EMOJI` — маппинг category_id → emoji.

---

### `diagnostic_scorer.py` — Диагностический скоринг

**Как работает:**
1. Загружает 10 вопросов из `diagnostic_questions.json`
2. Для каждого ответа суммирует баллы по 30 категориям
3. Нормализует в проценты (макс 100)
4. Берёт топ-5 категорий
5. Маппит категории на роли из `roles_database.json`
6. Возвращает топ-12 ролей

**Категории:** 30 штук (IT, дизайн, медицина, финансы и т.д.)

---

### `scenario_scorer.py` — Скоринг сценариев

**Как работает:**
- Каждый вариант ответа имеет `score` (0-20)
- Процент = (сумма баллов / макс. возможная) × 100
- Уровни: ≥80 "Отличный", ≥60 "Хороший", ≥40 "Средний", <40 "Нужно подтянуть"

---

### `async_analyzer.py` — Фоновый AI-анализ

**Как работает:**
1. После rule-based скоринга запускается в фоне (`asyncio.create_task`)
2. Отправляет ответы + результаты в AI (модель `stepfun/step-3.5-flash:free`)
3. Получает: strengths, weaknesses, recommendations, next_role
4. Сохраняет в таблицу `ai_analyses`
5. Доступен через `GET /api/roles/ai-analysis/{id}`

**Важно:** Не блокирует ответ пользователю — rule-based скоринг мгновенный (<50ms).

---

### `ai_service.py` — OpenRouter AI

**Модели:**
- Основная: `qwen/qwen3.6-plus:free`
- Fallback: `stepfun/step-3.5-flash:free`

**Функции:**
- `analyze_career()` — анализ карьеры
- `chat_with_ai()` — чат с контекстом
- `evaluate_match()` — оценка соответствия
- `quick_match_career()` — rule-based скоринг 16 ролей МТС
- `analyze_scenario_match()` — анализ сценариев
- `get_skill_recommendations()` — рекомендации по навыкам

---

### `hh_service.py` — HH.ru API

**Фичи:**
- Поиск вакансий через `api.hh.ru/vacancies`
- Кэш городов (TTL 1 час)
- Кэш результатов (TTL 5 минут)
- Rate limit handling (429 с exponential backoff)
- Парсинг key_skills из описания

---

## 9. Диагностический тест

### Файлы

| Файл | Описание |
|---|---|
| `backend/data/diagnostic_questions.json` | 10 вопросов с 5 вариантами |
| `backend/services/diagnostic_scorer.py` | Скоринг |
| `backend/api/onboarding.py` | API |
| `frontend/src/pages/DiagnosticTest.jsx` | UI |

### Поток

```
Пользователь заходит в Mini App
    ↓
/diagnostic — 10 вопросов (последовательно)
    ↓
POST /api/onboarding/diagnostic
    ↓
Ответ: топ-10 категорий + топ-12 ролей
    ↓
Сохранение в localStorage
    ↓
Экран результатов: категории + роли с эмодзи
    ↓
Клик на роль → /scenario-runner
```

### Структура вопроса

```json
{
  "id": "q1",
  "text": "Что тебе ближе всего?",
  "options": [
    {
      "text": "Создавать что-то новое с нуля",
      "scores": {
        "it_and_development": 8,
        "design_and_creative": 10,
        "media_and_entertainment": 7
      }
    }
  ]
}
```

Каждый вариант начисляет баллы 2-5 категориям. Максимум 100 баллов за тест.

---

## 10. Scenario Runner

### Файлы

| Файл | Описание |
|---|---|
| `frontend/src/pages/ScenarioRunner.jsx` | UI прохождения теста |
| `backend/api/roles.py` | API эндпоинты |
| `backend/services/scenario_scorer.py` | Rule-based скоринг |
| `backend/services/async_analyzer.py` | Фоновый AI |

### Поток

```
Пользователь выбирает роль(и)
    ↓
GET /api/roles/scenario/{role_id}?level=junior
    ↓
Загрузка сценария (5-10 вопросов)
    ↓
Последовательный показ вопросов
    ↓
Последний вопрос → POST /api/roles/score
    ↓
Мгновенный ответ (rule-based, <50ms)
    ↓
Фоновый AI-анализ (async)
    ↓
/dashbord с результатами
```

### Структура сценария

```json
{
  "role_id": "python_dev",
  "title": "Python-разработчик",
  "level": "junior",
  "description": "Базовый уровень",
  "questions": [
    {
      "id": "python_dev_j_q1",
      "text": "Что такое REST API?",
      "options": [
        {"text": "Архитектурный стиль", "score": 20},
        {"text": "Язык программирования", "score": 0}
      ]
    }
  ]
}
```

### Fallback localStorage

Если `location.state.roles` пустой (частая проблема в Telegram WebApp), ScenarioRunner загружает роли из `localStorage`:
```javascript
const stored = localStorage.getItem('pending_scenario_roles')
```

---

## 11. Данные

### `roles_database.json`

- **197 ролей** в 30 категориях
- Размер: ~60,000 строк JSON
- Каждая роль: role_id, title, category, category_id, skills[], salary{junior, middle}, scenarios{level: {questions[]}}

### `diagnostic_questions.json`

- **10 вопросов** с 5 вариантами ответов
- Каждый вариант → баллы 2-5 категориям

### `scenarios_primary.json`

- Сценарии для ролей МТС (8 ролей)

### `scenarios_from_hh.json`

- AI-сгенерированные сценарии на основе HH.ru

### `hh_requirements.json`

- Требования из вакансий HH.ru по ролям

---

## 12. Настройка окружения

### `.env` файл

Скопируйте `.env.example` в `.env` и заполните:

```env
# OpenRouter API (бесплатные модели)
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=qwen/qwen3.6-plus:free
OPENROUTER_MODEL_FALLBACK=stepfun/step-3.5-flash:free

# Telegram Bot
TG_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# HH.ru API (User-Agent для запросов)
HH_USER_AGENT=MyCareerBot/1.0 (your@email.com)

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173

# Database
DATABASE_PATH=career_navigator.db
```

**Где получить ключи:**
- **OpenRouter:** https://openrouter.ai/keys (бесплатный, без карты)
- **Telegram Bot:** @BotFather → `/newbot`
- **HH.ru:** Не требует ключа для публичного API

### `VITE_API_URL`

Фронтенд читает из `.env` (или env variables при билде):
```env
VITE_API_URL=http://localhost:8000/api
```

---

## 13. Запуск проекта

### 1. Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### 2. Запуск (3 терминала)

| Терминал | Команда | Порт |
|---|---|---|
| **Backend** | `cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000` | 8000 |
| **Frontend** | `cd frontend && npm run dev` | 5173 |
| **Bot** (опционально) | `cd bot && python bot.py` | — |

### 3. Проверка

```bash
# Backend health
curl http://localhost:8000/api/health
# → {"status": "ok", "service": "AI Career Navigator"}

# Diagnostic questions
curl http://localhost:8000/api/onboarding/questions
# → {"questions": [...], "count": 10}

# Frontend
open http://localhost:5173
```

### 4. Swagger UI

```
http://localhost:8000/docs
```

Все эндпоинты с возможностью тестирования прямо в браузере.

---

## 14. Пользовательские потоки

### Основной поток (новый)

```
1. Первый вход в Mini App
       ↓
2. /diagnostic — 10 вопросов (30-60 сек)
       ↓
3. Результаты: топ-3 категории + 8-12 ролей
       ↓
4. Выбор роли → клик
       ↓
5. /scenario-runner — 5-10 вопросов
       ↓
6. Мгновенный результат + AI-анализ в фоне
       ↓
7. /dashboard — профиль, результаты, рекомендации
       ↓
8. /career — все роли, повторные тесты
       ↓
9. /vacancies — поиск вакансий HH.ru
       ↓
10. /chat — AI-наставник
```

### Альтернативный поток (через онбординг)

```
1. /onboarding — 3 шага (образование, профессия, опыт)
       ↓
2. /diagnostic — уточняющий тест
       ↓
3. Далее как основной поток
```

### Перетест

```
1. /dashboard → кнопка "Пройти заново"
       ↓
2. Проверка кулдауна (7 дней)
       ↓
3. /diagnostic → новый тест
```

---

## 15. Деплой

### Backend (production)

```bash
# Установка
pip install -r requirements.txt

# Запуск с uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Или через gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend (production)

```bash
# Build
cd frontend
npm run build

# Результат в frontend/dist/
# Раздавать через nginx или любой static hosting
```

### nginx конфиг (пример)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend (static)
    location / {
        root /var/www/career-navigator/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Telegram Mini App

1. Создать бота через @BotFather
2. `/newapp` → указать URL (https://your-domain.com)
3. В `index.html` указать правильный URL API

---

## 16. FAQ и частые проблемы

### Проблема: Scenario Runner не открывается при клике на роль

**Причина:** `location.state` теряется при навигации в Telegram WebApp.

**Решение:** ScenarioRunner теперь использует fallback на `localStorage`:
```javascript
localStorage.setItem('pending_scenario_roles', JSON.stringify([role]))
```

Убедитесь, что в `DiagnosticTest.jsx` есть сохранение в localStorage при клике на роль.

---

### Проблема: Вопросы сценария отображаются как объекты `{text, score}` вместо строк

**Причина:** Структура вопросов в БД — объекты, а не строки.

**Решение:** В `ScenarioRunner.jsx` добавлена обработка:
```javascript
const optionText = typeof option === 'string' ? option : option.text
```

---

### Проблема: После прохождения теста редирект обратно на diagnostic

**Причина:** Сценарий для роли не найден или пустой.

**Диагностика:** Проверить console.log в ScenarioRunner:
```
📦 Loading scenarios for roles: ['python_dev']
📋 Scenario for python_dev: {...}
```

Если `⚠️ No scenario for python_dev` — проверить наличие сценария в `roles_database.json`.

---

### Проблема: Пустой список ролей после диагностики

**Причина:** Профиль пустой или category_id не маппится.

**Решение:**
1. Проверить `diagnostic_questions.json` — все category_id должны быть в `CATEGORY_EMOJI`
2. Проверить `roles_database.json` — у ролей должен быть `category_id`
3. Минимальный порог в `diagnostic_scorer.py`: `if percent >= 5`

---

### Проблема: AI-анализ не появляется в результатах

**Причина:** AI-анализ работает в фоне и может занять 5-15 секунд.

**Решение:**
1. Проверить `GET /api/roles/ai-analysis/{telegram_id}` — если `{"status": "pending"}`, подождать
2. Проверить логи backend — ошибки OpenRouter API
3. Проверить `OPENROUTER_API_KEY` в `.env`

---

### Проблема: HH.ru вакансии не загружаются

**Причина:** Rate limit или неверный User-Agent.

**Решение:**
1. Указать корректный `HH_USER_AGENT` в `.env`
2. Кэш работает автоматически (TTL 5 минут)
3. Проверить `GET /api/vacancies/search?profession=Python&location=Москва`

---

### Проблема: Порт 8000 или 5173 уже занят

**Решение:**
```bash
# Windows — найти процесс
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Или сменить порт
uvicorn main:app --port 8001
# В vite.config.js: server: { port: 5174 }
```

---

### Проблема: Telegram WebApp не видит `window.Telegram.WebApp`

**Решение:** Убедитесь, что в `index.html` подключён SDK:
```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
```

И приложение открыто через Telegram, а не в браузере.

---

### Проблема: CORS ошибки

**Решение:** В `main.py` уже настроен CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production заменить на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📎 Полезные ссылки

| Ресурс | URL |
|---|---|
| OpenRouter | https://openrouter.ai |
| HH.ru API Docs | https://github.com/hhru/api |
| Telegram Bot API | https://core.telegram.org/bots/api |
| Telegram Mini Apps | https://core.telegram.org/bots/webapps |
| FastAPI Docs | https://fastapi.tiangolo.com |
| React Router | https://reactrouter.com |

---

## 📞 Контакты

По вопросам разработки обращайтесь к команде проекта.

---

*Документация обновлена: Апрель 2026*

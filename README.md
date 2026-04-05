# 🧠 CareerFlow

> **CareerFlow** — AI-карьерный навигатор в формате Telegram Mini App.
> Диагностика навыков, 197 профессий, интерактивные тесты-сценарии, AI-анализ и рекомендации.

---

## 📋 Содержание

1. [Что умеет](#-что-умеет)
2. [Архитектура](#-архитектура)
3. [Быстрый старт](#-быстрый-старт)
4. [Структура проекта](#-структура-проекта)
5. [Backend API](#-backend-api)
6. [База данных](#-база-данных)
7. [Фронтенд](#-фронтенд)
8. [Сервисы](#-сервисы)
9. [Telegram бот](#-telegram-бот)
10. [Переменные окружения](#-переменные-окружения)
11. [Деплой](#-деплой)
12. [Troubleshooting](#-troubleshooting)

---

## 🎯 Что умеет

### 🔍 Диагностика
- **10 вопросов** — определение подходящих категорий и ролей
- Автоматический скоринг по **30 категориям** (IT, дизайн, финансы и др.)
- Рекомендация **топ-12 профессий** из базы 197 ролей

### 🎮 Тесты-сценарии
- **197 ролей** с уникальными вопросами и ситуациями
- Мгновенный **rule-based скоринг** (< 50ms)
- Фоновый **AI-анализ** результатов (сильные/слабые стороны, рекомендации)
- Уровни: Junior / Middle

### 🔥 Daily Challenge
- Ежедневная ситуация для прокачки
- AI-оценка ответа
- **Streak-система** (серия дней подряд)

### 🏆 Достижения
- **16 бейджей**: первый шаг, streak 3/7/30 дней, перфекционист, отличник и др.
- Автоматическая разблокировка

### 💼 Вакансии HH.ru
- Поиск реальных вакансий через `api.hh.ru`
- Матчинг с навыками пользователя
- Зарплатные вилки, недостающие навыки

### 💬 AI-наставник (чат)
- Персональные ответы о карьере с учётом профиля
- Сохранение истории чата (контекст 5 сообщений)

### 📊 Профиль и лидерборд
- Онбординг: образование, опыт, навыки, интересы, цели
- Рейтинг пользователей по среднему баллу
- Перетест с кулдауном 7 дней

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram Mini App                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │◄──►│  React +     │◄──►│ Vite Dev     │  │
│  │   (SPA)      │    │  Vite        │    │ Server :5173 │  │
│  └──────┬───────┘    └──────────────┘    └──────────────┘  │
│         │ HTTP/JSON                                          │
│         ▼                                                    │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │◄──►│  FastAPI     │◄──►│ Uvicorn      │  │
│  │   API        │    │  :8000       │    │ Server       │  │
│  └──────┬───────┘    └──────────────┘    └──────────────┘  │
│         │                                                    │
│    ┌────┴────┬────────────┬──────────┐                     │
│    ▼         ▼            ▼          ▼                     │
│  ┌──────┐ ┌──────┐ ┌──────────┐ ┌──────────┐              │
│  │SQLite│ │Open- │ │ HH.ru    │ │ Telegram │              │
│  │  DB  │ │Router│ │ API      │ │ Bot API  │              │
│  └──────┘ └──────┘ └──────────┘ └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Быстрый старт

### 1. Настройка окружения

```bash
cp .env.example .env   # или создать .env вручную
```

Заполнить `.env` (см. раздел [Переменные окружения](#-переменные-окружения)).

### 2. Установка зависимостей

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Запуск (3 терминала)

| Терминал | Команда | Порт |
|----------|---------|------|
| **Backend** | `cd backend && uvicorn main:app --reload --port 8000` | 8000 |
| **Frontend** | `cd frontend && npm run dev` | 5173 |
| **Bot** (опционально) | `cd bot && python bot.py` | — |

### 4. Проверка

```bash
# Backend health
curl http://localhost:8000/api/health
# → {"status": "ok", "service": "CareerFlow"}

# Diagnostic questions
curl http://localhost:8000/api/onboarding/questions
# → {"questions": [...], "count": 10}

# Frontend
open http://localhost:5173
```

---

## 📁 Структура проекта

```
c:\vscode\elkincode\
├── .env                          # Секретные ключи (НЕ коммитить!)
├── .gitignore
├── amvera.yml                    # Конфиг деплоя на Amvera
├── main.py                       # Точка входа для деплоя (backend + bot)
├── requirements.txt              # Python зависимости
├── README.md                     # Этот файл
├── DEV_DOCS.md                   # Полная документация разработчика
│
├── backend/                      # FastAPI сервер
│   ├── main.py                   # FastAPI приложение (CORS, роуты, startup)
│   ├── server.py                 # Unified: FastAPI + Telegram бот в одном процессе
│   ├── bot.py                    # Telegram бот (автономный запуск)
│   ├── api/                      # API роутеры (11 штук)
│   │   ├── __init__.py
│   │   ├── user.py               # Профиль, онбординг, статистика
│   │   ├── career.py             # AI анализ карьеры
│   │   ├── vacancies.py          # HH.ru вакансии
│   │   ├── chat.py               # AI чат-наставник
│   │   ├── scenarios.py          # Сценарии, лидерборд, перетест
│   │   ├── roles.py              # Rule-based матчинг, скоринг, AI-анализ
│   │   ├── onboarding.py         # Диагностика, вопросы, рекомендации
│   │   ├── daily_challenge.py    # Ежедневные челленджи, streak
│   │   ├── achievements.py       # Бейджи/достижения
│   │   └── telegram_api.py       # Telegram WebApp auth, валидация, аватар
│   ├── database/
│   │   └── db.py                 # SQLite async (12 таблиц)
│   ├── models/
│   │   └── models.py             # Pydantic модели
│   ├── services/                 # Бизнес-логика
│   │   ├── __init__.py
│   │   ├── ai_service.py         # OpenRouter AI (основная + fallback)
│   │   ├── role_matcher.py       # Rule-based матчинг ролей (0-100 баллов)
│   │   ├── scenario_scorer.py    # Скоринг сценариев (ситуация + тест)
│   │   ├── diagnostic_scorer.py  # Диагностический скоринг (10 вопросов)
│   │   ├── daily_challenge_service.py  # AI-генерация daily challenge
│   │   ├── achievement_service.py       # Система бейджей (16 штук)
│   │   ├── hh_service.py                # HH.ru API клиент с кэшем
│   │   ├── matching_service.py          # Матчинг вакансий (AI + simple)
│   │   ├── async_analyzer.py            # Фоновый AI-анализ сценариев
│   │   └── telegram_auth.py             # HMAC-SHA256 валидация initData
│   ├── data/                     # Статические данные
│   │   ├── roles_database.json       # 197 ролей в 30 категориях
│   │   ├── diagnostic_questions.json # 10 вопросов с баллами
│   │   ├── scenarios_primary.json    # Первичные сценарии
│   │   ├── scenarios_from_hh.json    # Сценарии из HH.ru
│   │   └── hh_requirements.json      # Требования из HH.ru
│   └── scripts/
│       ├── roles_data.py             # Исходные данные 300+ ролей
│       └── generate_roles_db.py      # Генератор roles_database.json
│
├── frontend/                     # React SPA (Vite)
│   ├── index.html                # Точка входа + Telegram WebApp SDK
│   ├── package.json              # Node зависимости
│   ├── vite.config.js            # Dev-сервер + прокси /api
│   └── src/
│       ├── main.jsx              # Точка входа React
│       ├── App.jsx               # Роутинг + Telegram Context
│       ├── index.css             # Стили (тёмная тема + MTS дизайн)
│       ├── api/
│       │   └── client.js         # API клиент (~35 методов)
│       ├── hooks/
│       │   └── useTelegramAuth.js # Хук авторизации
│       ├── components/
│       │   └── BottomNav.jsx      # Нижняя навигация (4 вкладки)
│       └── pages/
│           ├── DiagnosticTest.jsx # Диагностика (10 вопросов)
│           ├── ScenarioRunner.jsx # Тест-сценарий
│           ├── CareerPath.jsx     # Карьерный путь + результаты
│           ├── RoleSelection.jsx  # Выбор ролей
│           ├── Onboarding.jsx     # Упрощённый онбординг (3 шага)
│           ├── Dashboard.jsx      # Профиль + daily + достижения
│           ├── Vacancies.jsx      # Поиск вакансий HH.ru
│           └── Chat.jsx           # AI-наставник
│
└── bot/
    └── bot.py                    # Telegram бот (/start, /help, daily reminders)
```

---

## 🔌 Backend API

### Health Check
```
GET /api/health
→ {"status": "ok", "service": "CareerFlow"}
```

### User (`/api/user`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/user/onboarding` | Сохранение данных онбординга |
| GET | `/api/user/profile/{telegram_id}` | Получение профиля |
| GET | `/api/user/stats/{telegram_id}` | Статистика профиля |

### Onboarding/Diagnostic (`/api/onboarding`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/onboarding/questions` | 10 диагностических вопросов |
| POST | `/api/onboarding/diagnostic` | Запуск диагностики |
| GET | `/api/onboarding/diagnostic-result/{telegram_id}` | Результат диагностики |
| POST | `/api/onboarding/save-profile` | Сохранение профиля |

### Roles (`/api/roles`) — rule-based матчинг
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/roles/match` | Матчинг ролей для пользователя |
| GET | `/api/roles/all` | Все 197 ролей |
| GET | `/api/roles/search?q=` | Поиск ролей |
| GET | `/api/roles/scenario/{role_id}?level=` | Сценарий для роли |
| POST | `/api/roles/score` | Скоринг ответов (rule-based, < 50ms) |
| GET | `/api/roles/ai-analysis/{telegram_id}` | Фоновый AI-анализ |

### Scenarios (`/api/scenarios`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/scenarios/my-scenarios/{telegram_id}` | Результаты пользователя |
| GET | `/api/scenarios/leaderboard` | Топ по среднему баллу |
| GET | `/api/scenarios/retest-status/{telegram_id}` | Статус перетеста |
| POST | `/api/scenarios/retest-start/{telegram_id}` | Начало перетеста |
| POST | `/api/scenarios/retest-complete/{telegram_id}` | Завершение перетеста |
| POST | `/api/scenarios/scenarios/save-answers` | Сохранение ответов |

### Career (`/api/career`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/career/analyze` | AI анализ карьеры |
| GET | `/api/career/result/{telegram_id}` | Результат анализа |
| POST | `/api/career/quick-match` | Быстрый матчинг |

### Vacancies (`/api/vacancies`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/vacancies/search?profession=&location=&limit=` | Поиск на HH.ru |
| POST | `/api/vacancies/match` | Матчинг вакансий |
| GET | `/api/vacancies/mts` | Вакансии МТС |

### Chat (`/api/chat`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/chat/message` | Сообщение в AI-чат |
| GET | `/api/chat/history/{telegram_id}` | История чата |

### Daily Challenge (`/api/daily`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/daily/challenge?telegram_id=` | Ситуация дня |
| POST | `/api/daily/answer` | Ответ на ситуацию |
| GET | `/api/daily/streak?telegram_id=` | Текущая серия |

### Achievements (`/api/achievements`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/achievements/list?telegram_id=` | Список достижений |

### Telegram (`/api/telegram`)
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/telegram/auth` | Авторизация через initData |
| GET | `/api/telegram/avatar/{telegram_id}` | Аватар через Bot API |
| GET | `/api/telegram/profile/{telegram_id}` | Профиль Telegram |

---

## 🗄 База данных

**Движок:** SQLite (async через `aiosqlite`)
**Файл:** `career_navigator.db` (создаётся автоматически)

### 12 таблиц

| Таблица | Описание |
|---------|----------|
| `users` | Профиль пользователя |
| `career_analyses` | AI-анализы карьеры |
| `vacancy_matches` | Матчинг вакансий |
| `chat_history` | История чата с AI |
| `scenario_results` | Результаты сценариев |
| `retest_cooldowns` | Кулдаун перетеста (7 дней) |
| `scenario_answers` | Сырые ответы (ждут AI-анализа) |
| `generated_scenarios` | Кэш AI-сценариев |
| `ai_analyses` | AI-анализы результатов сценариев |
| `daily_challenges` | Ежедневные челленджи + ответы |
| `user_achievements` | Разблокированные бейджи |
| `diagnostic_results` | Результаты диагностики |

---

## 🎨 Фронтенд

### Роутинг

| Путь | Компонент | BottomNav |
|------|-----------|-----------|
| `/` | → `/diagnostic` | — |
| `/diagnostic` | `DiagnosticTest` | — |
| `/onboarding` | `Onboarding` | — |
| `/role-selection` | `RoleSelection` | — |
| `/scenario-runner` | `ScenarioRunner` | — |
| `/career` | `CareerPath` | ✅ |
| `/dashboard` | `Dashboard` | ✅ |
| `/vacancies` | `Vacancies` | ✅ |
| `/chat` | `Chat` | ✅ |

### API клиент (`src/api/client.js`)

```javascript
import { api } from '../api/client'

// Примеры
const questions = await api.getDiagnosticQuestions()
const result = await api.runDiagnostic(answers)
const roles = await api.matchRoles()
const scenario = await api.getScenario('python_dev', 'junior')
const score = await api.scoreScenario('python_dev', 'junior', answers)
const vacancies = await api.searchVacancies('Python', 'Москва')
```

### Дизайн

- **Тёмная тема** — фон `#18181B`, карточки `#27272A`
- **MTS Red** `#E30611` — акцентный цвет
- Градиенты, красное свечение, адаптив для мобильных

---

## ⚙️ Сервисы

### `diagnostic_scorer.py`
10 вопросов → баллы по 30 категориям → топ-5 → маппинг на 197 ролей → топ-12 рекомендаций.

### `role_matcher.py`
Скоринг 0-100: навыки (0-30) + поле (0-30) + интересы (0-20) + опыт (0-20). Порог: 10 баллов.

### `scenario_scorer.py`
Rule-based: каждый вариант = 0-20 баллов. Процент = (сумма / макс) × 100.
Уровни: ≥80 «Отличный», ≥60 «Хороший», ≥40 «Средний», <40 «Нужно подтянуть».

### `async_analyzer.py`
Фоновый AI-анализ после скоринга. Не блокирует ответ (< 50ms rule-based).
Сохраняет: strengths, weaknesses, recommendations, next_role.

### `ai_service.py`
OpenRouter AI с fallback:
- Основная: `qwen/qwen3.6-plus:free`
- Fallback: `stepfun/step-3.5-flash:free`
- Автопереключение при ошибках + демо-данные при недоступности.

### `hh_service.py`
Поиск вакансий через `api.hh.ru`. Кэш городов (TTL 1ч), кэш результатов (TTL 5мин), retry при 429.

### `daily_challenge_service.py`
AI-генерация ситуации дня, оценка ответа, streak-система.

### `achievement_service.py`
16 бейджей: `first_diagnostic`, `first_test`, `high_avg`, `streak_3`, `streak_7`, `streak_30`, `test_5`, `test_10`, `perfectionist` и др.

### `telegram_auth.py`
HMAC-SHA256 валидация `initData` (официальный алгоритм Telegram). Fallback non-strict для разработки.

---

## 🤖 Telegram бот

### Команды
| Команда | Описание |
|---------|----------|
| `/start` | Приветствие + кнопка «Открыть CareerFlow» |
| `/help` | Инструкция по использованию |

### Daily Reminders
Ежедневная рассылка в 10:00 всем пользователям из БД.

### Режимы запуска
1. **Вместе с API** — `python server.py` (бот в daemon-потоке)
2. **Отдельно** — `python bot.py` (polling в async loop)
3. **Для деплоя** — `python main.py` из корня (alias на `server.py`)

---

## 🔑 Переменные окружения

### `.env` (корень проекта)

> **Для локальной разработки** — значения по умолчанию уже настроены.

| Переменная | Обязательно | Описание | Значение по умолчанию |
|---|---|---|---|
| `OPENROUTER_API_KEY` | ✅ | Ключ OpenRouter AI | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | | Основная модель | `qwen/qwen3.6-plus:free` |
| `OPENROUTER_MODEL_FALLBACK` | | Резервная модель | `stepfun/step-3.5-flash:free` |
| `TG_BOT_TOKEN` | ✅ | Токен Telegram бота | `123456:ABC...` |
| `HH_USER_AGENT` | ✅ | User-Agent для HH.ru | `Mozilla/5.0 ...` |
| `BACKEND_URL` | | URL бэкенда | `http://localhost:8000` |
| `FRONTEND_URL` | | URL фронтенда | `http://localhost:5173` |
| `WEBAPP_URL` | | URL Mini App (для продакшена) | `https://webtoelkin.vercel.app` |
| `DATABASE_PATH` | | Путь к SQLite БД | `career_navigator.db` |

### Где получить ключи

| Сервис | URL | Стоимость |
|---|---|---|
| OpenRouter | https://openrouter.ai/keys | Бесплатно, без карты |
| Telegram Bot | @BotFather → `/newbot` | Бесплатно |
| HH.ru | Не требует ключа | Бесплатно |

---

## 🛠 Технологии

### Backend
| Технология | Версия | Назначение |
|---|---|---|
| Python | 3.10+ | Язык |
| FastAPI | 0.115+ | REST API |
| Uvicorn | 0.30+ | ASGI сервер |
| AsyncOpenAI | 1.50+ | OpenRouter AI |
| HTTPX | 0.27+ | Асинхронные HTTP |
| AioSQLite | 0.20+ | Async SQLite |
| Pydantic | 2.10+ | Валидация |
| python-dotenv | 1.0+ | Загрузка .env |
| python-telegram-bot | 21.6+ | Telegram бот |

### Frontend
| Технология | Версия | Назначение |
|---|---|---|
| React | 18.3+ | UI |
| Vite | 5.4+ | Сборка + dev сервер |
| React Router | 6.26+ | Роутинг |
| Telegram WebApp SDK | 7.0+ | Интеграция |

---

## 🚀 Деплой (продакшен)

> Проект уже настроен для деплоя на **Amvera** (бэкенд) и **Vercel** (фронтенд).
> Для переключения на продакшен — обновите `.env` и `frontend/src/api/client.js`.

### Backend → Amvera

**amvera.yml** уже настроен:
```yaml
meta:
  environment: python
  toolchain:
    name: pip
    version: 3.13
build:
  requirementsPath: requirements.txt
run:
  scriptName: main.py
  persistenceMount: /data
  containerPort: 8000
```

**Что изменить при деплое:**
1. В `.env` → `BACKEND_URL=https://your-app.amvera.io`
2. В `frontend/src/api/client.js` → `const API_BASE = 'https://your-app.amvera.io/api'`
3. В панели Amvera → Environment Variables → добавить все ключи из `.env`
4. `DATABASE_PATH=/data/career_navigator.db` (для persist БД)

### Frontend → Vercel

```bash
cd frontend
npm run build
vercel --prod
```

**Environment Variable в Vercel:**
```
VITE_API_URL=https://your-backend.amvera.io/api
```

---

## 🐛 Troubleshooting

### AI не работает (Connection error)
1. **Amvera может блокировать** `openrouter.ai` — проверить через `curl` с сервера
2. **Rate limit** — free модели имеют ограничения, подождать 1-2 минуты
3. **Проверить ключ:**
   ```bash
   curl -X POST https://openrouter.ai/api/v1/chat/completions \
     -H "Authorization: Bearer YOUR_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen/qwen3.6-plus:free","messages":[{"role":"user","content":"test"}]}'
   ```
4. **Демо-режим** — сервисы возвращают демо-данные при недоступности AI

### Порт 8000 занят
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### БД не создаётся
- Локально: `DATABASE_PATH=career_navigator.db` (без `/data/`) — уже настроено
- На Amvera: `DATABASE_PATH=/data/career_navigator.db` + `persistenceMount: /data`

### Frontend не подключается к бэкенду
- Проверить `API_BASE` в `frontend/src/api/client.js` → `http://localhost:8000/api`
- Убедиться, что CORS настроен (`allow_origins=["*"]`)
- `curl http://localhost:8000/api/health` → `{"status": "ok"}`

### Telegram бот не запускается
- Проверить токен: `python -c "import os; from dotenv import load_dotenv(); load_dotenv(); print(os.getenv('TG_BOT_TOKEN'))"`
- Убедиться, что бот активен через @BotFather
- Логи: `python bot.py` → «🤖 Бот запущен!»


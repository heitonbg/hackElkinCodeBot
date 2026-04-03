# 🧠 AI Career Navigator — МТС

> **AI-карьерный навигатор** с интеллектуальным наставником в формате Telegram Mini App.  
> Персональный AI анализирует навыки, подбирает профессии и строит карьерный путь.

---

## 📋 Содержание

1. [Что умеет бот](#-что-умеет-бот)
2. [Быстрый старт](#-быстрый-старт)
3. [Структура проекта](#-структура-проекта)
4. [Описание файлов](#-описание-файлов)
5. [API ключи](#-api-ключи)
6. [Технологии](#-технологии)
7. [Дизайн МТС](#-дизайн-мс)
8. [Деплой](#-деплой)

---

## 🎯 Что умеет бот

### 🧠 AI-анализ карьеры
- Анализирует навыки, интересы и опыт пользователя
- Подбирает **5 подходящих профессий** с процентом совпадения
- Указывает **зарплатные вилки** для каждой позиции
- Формирует **пошаговый карьерный путь** (4 этапа)
- Даёт **конкретные рекомендации** (курсы, проекты, сообщества)
- Определяет **недостающие навыки** для роста

### 💬 AI-наставник (чат)
- Отвечает на вопросы о карьере и развитии
- Учитывает профиль пользователя для персонализации
- Сохраняет историю чата (5 сообщений контекста)
- Рекомендует ресурсы, курсы и проекты

### 💼 Вакансии
- **Вакансии МТС** из внутренней матрицы компетенций
- **Матчинг** пользователя с вакансиями МТС (AI оценивает совпадение навыков)
- **Поиск на HH.ru** — реальные вакансии с рынка
- Фильтрация по профессии и локации

### 📊 Профиль пользователя
- Онбординг из 6 шагов (образование, направление, опыт, интересы, навыки, цели)
- Статистика заполненности профиля
- Отображение навыков, интересов и карьерных целей

---

## 🚀 Быстрый старт

### 1. Настройка окружения
```bash
# Скопировать шаблон
cp .env.example .env

# Заполнить .env своими ключами (см. раздел API ключи ниже)
```

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

### 3. Запуск

Откройте **3 терминала**:

| Терминал | Команда | Что запускает |
|----------|---------|---------------|
| **1** | `cd backend && uvicorn main:app --reload --port 8000` | FastAPI сервер |
| **2** | `cd frontend && npm run dev` | React приложение (Vite) |
| **3** | `cd bot && python bot.py` | Telegram бот |

### 4. Проверка

| Сервис | URL | Ожидание |
|--------|-----|----------|
| Backend | http://localhost:8000/api/health | `{"status": "ok"}` |
| Frontend | http://localhost:5173 | Страница онбординга |
| Bot | Telegram → `@your_bot` | Команда `/start` работает |

---

## 📁 Структура проекта

```
c:\vscode\elkincode\
├── .env                      # Конфигурация (API ключи, URL-адреса)
├── .env.example              # Шаблон конфигурации
├── .gitignore                # Игнорируемые файлы
├── requirements.txt          # Python зависимости
├── README.md                 # Этот файл
│
├── backend/                  # FastAPI сервер
│   ├── main.py               # Точка входа, маршруты, CORS
│   ├── database/             # База данных
│   │   └── db.py             # SQLite + aiosqlite (users, analyses, chat_history)
│   ├── models/               # Pydantic модели
│   │   └── models.py         # UserProfile, OnboardingData, ChatMessage и др.
│   ├── api/                  # API роуты
│   │   ├── user.py           # Онбординг, профиль, статистика
│   │   ├── career.py         # AI анализ карьеры
│   │   ├── chat.py           # AI чат
│   │   └── vacancies.py      # Поиск вакансий (МТС + HH.ru)
│   └── services/             # Бизнес-логика
│       ├── ai_service.py     # OpenRouter AI (Qwen3.6 Plus)
│       ├── hh_service.py     # HH.ru API
│       ├── matching_service.py   # AI матчинг вакансий
│       ├── mts_vacancies.py      # Матрица вакансий МТС
│       └── mts_matching.py       # Матчинг с вакансиями МТС
│
├── frontend/                 # React приложение (Vite)
│   ├── index.html            # HTML шаблон + Telegram WebApp SDK
│   ├── package.json          # Node зависимости
│   ├── vite.config.js        # Конфиг Vite
│   └── src/
│       ├── main.jsx          # Точка входа React
│       ├── App.jsx           # Роутинг (React Router)
│       ├── index.css         # Стили (дизайн МТС)
│       ├── api/
│       │   └── client.js     # API клиент (fetch, telegram_id)
│       ├── components/
│       │   └── BottomNav.jsx # Нижняя навигация (4 вкладки)
│       └── pages/
│           ├── Onboarding.jsx    # Онбординг (6 шагов)
│           ├── Dashboard.jsx     # Профиль + AI анализ
│           ├── CareerPath.jsx    # Карьерный путь
│           ├── Vacancies.jsx     # Вакансии (МТС + HH.ru)
│           └── Chat.jsx          # AI чат
│
└── bot/                      # Telegram бот
    └── bot.py                # /start, /help команды + Mini App ссылка
```

---

## 📄 Описание файлов

### 🔧 Корень проекта

| Файл | Назначение |
|------|------------|
| `.env` | **Конфигурация проекта** — API ключи, URL-адреса, настройки БД |
| `.env.example` | **Шаблон** — пример заполнения `.env` |
| `.gitignore` | Исключает `.env`, `node_modules`, `__pycache__`, `.db` |
| `requirements.txt` | Python пакеты: FastAPI, openai, httpx, aiosqlite и др. |
| `README.md` | Документация проекта |
| `START.md` | Краткая инструкция по запуску |

---

### ⚙️ Backend (`backend/`)

#### `main.py` — Сервер
- Создание FastAPI приложения
- Настройка CORS для React
- Подключение базы данных при старте
- Регистрация роутов (`/api/user`, `/api/career`, `/api/chat`, `/api/vacancies`)
- Health-check endpoint: `/api/health`

#### `database/db.py` — База данных
- **SQLite** через `aiosqlite` (асинхронный)
- Таблицы:
  - `users` — профиль пользователя (образование, навыки, интересы, цели)
  - `career_analyses` — результаты AI анализа карьеры
  - `vacancy_matches` — матчинг вакансий
  - `chat_history` — история сообщений с AI
- CRUD операции для каждой таблицы

#### `models/models.py` — Pydantic модели
- `UserProfile` — данные профиля
- `OnboardingData` — данные онбординга
- `CareerAnalysis` — запрос на анализ
- `VacancyFilter` — фильтр для поиска вакансий
- `ChatMessage` — сообщение в чат

#### `api/user.py` — Пользователь
| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/user/onboarding` | POST | Сохранение данных онбординга |
| `/api/user/profile/{telegram_id}` | GET | Получение профиля |
| `/api/user/stats/{telegram_id}` | GET | Статистика (заполненность, кол-во навыков) |

#### `api/career.py` — Карьера
| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/career/analyze` | POST | Запуск AI анализа карьеры |
| `/api/career/result/{telegram_id}` | GET | Получение результатов анализа |

#### `api/chat.py` — Чат
| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/chat/message` | POST | Отправка сообщения в AI |
| `/api/chat/history/{telegram_id}` | GET | История чата (последние 20) |

#### `api/vacancies.py` — Вакансии
| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/vacancies/search` | GET | Поиск на HH.ru |
| `/api/vacancies/mts` | GET | Вакансии МТС |
| `/api/vacancies/mts/match/{telegram_id}` | GET | Матчинг с вакансиями МТС |
| `/api/vacancies/match` | POST | Матчинг с HH.ru вакансиями |

#### `services/ai_service.py` — AI сервис
- **OpenRouter API** (OpenAI-compatible)
- Модели: Qwen3.6 Plus (основная), Step 3.5 Flash (fallback)
- Функции:
  - `analyze_career()` — анализ карьеры → JSON с профессиями, путём, навыками
  - `chat_with_ai()` — чат с AI с контекстом пользователя
  - `evaluate_match()` — оценка соответствия навыкам вакансии
  - `_call_openai_with_fallback()` — автоматическое переключение при ошибках

#### `services/hh_service.py` — HH.ru API
- Поиск вакансий через `api.hh.ru`
- Форматирование зарплат
- Извлечение требований из описания

#### `services/matching_service.py` — AI матчинг
- Оценка соответствия навыков пользователя требованиям вакансии
- Использование AI для расчёта match_score

#### `services/mts_vacancies.py` — Вакансии МТС
- Статическая матрица компетенций МТС
- IT и не-IT вакансии с уровнями

#### `services/mts_matching.py` — Матчинг МТС
- Сопоставление навыков пользователя с требованиями вакансий МТС
- Расчёт процента совпадения

---

### 🎨 Frontend (`frontend/`)

#### `index.html` — HTML шаблон
- Подключение **Telegram WebApp SDK**
- Мета-теги для мобильных
- Точка входа для React

#### `src/main.jsx` — Точка входа
- Рендеринг `<App />` в `#root`

#### `src/App.jsx` — Роутинг
| Путь | Компонент | Описание |
|------|-----------|----------|
| `/` | Onboarding | Онбординг (6 шагов) |
| `/dashboard` | Dashboard | Профиль + AI анализ |
| `/career` | CareerPath | Карьерный путь |
| `/vacancies` | Vacancies | Вакансии |
| `/chat` | Chat | AI чат |

#### `src/index.css` — Стили
- **Дизайн МТС** — красный `#E30611`, градиенты, тени
- Адаптивные карточки, кнопки, теги
- Анимации hover, spinner, переходы
- Telegram theme variables

#### `src/api/client.js` — API клиент
- `getTelegramId()` — извлекает ID из Telegram WebApp
- `request()` — обёртка над `fetch` с обработкой ошибок
- Методы: `saveOnboarding`, `analyzeCareer`, `sendMessage` и др.

#### `src/components/BottomNav.jsx` — Навигация
- 4 вкладки: Профиль 📊, Карьера 🚀, Вакансии 💼, Чат 💬
- Индикатор активной вкладки (красная точка МТС)

#### `src/pages/Onboarding.jsx` — Онбординг
- 6 шагов с прогресс-баром
- Типы: select (один вариант), multi (несколько)
- Кнопка «Пропустить и посмотреть демо»

#### `src/pages/Dashboard.jsx` — Профиль
- Отображение профиля (образование, направление, опыт)
- Навыки и интересы (теги)
- AI анализ (профессии, зарплаты, рекомендации)
- Кнопка «Начать AI-анализ»

#### `src/pages/CareerPath.jsx` — Карьерный путь
- 4 шага карьерного развития с длительностью
- Навыки для развития
- Рекомендации с конкретными действиями

#### `src/pages/Vacancies.jsx` — Вакансии
- Табы: Вакансии МТС / Поиск HH.ru
- Матчинг с процентом совпадения
- Показ matching/missing навыков
- Ссылки на HH.ru

#### `src/pages/Chat.jsx` — Чат
- Список сообщений (user/AI)
- Поле ввода с кнопкой отправки
- Авто-скролл к новым сообщениям
- Индикатор загрузки

---

### 🤖 Bot (`bot/`)

#### `bot.py` — Telegram бот
- **Команда `/start`** — приветствие + ссылка на Mini App
- **Команда `/help`** — инструкция по использованию
- Ссылка на frontend в Mini App
- Логирование действий

---

## 🔑 API ключи

### OpenRouter (AI)
1. Зарегистрироваться: https://openrouter.ai
2. Создать API ключ (бесплатно)
3. Вставить в `.env`:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx
   ```

**Рекомендуемые модели:**
| Модель | ID | Рейтинг | Описание |
|--------|------|---------|----------|
| Qwen3.6 Plus | `qwen/qwen3.6-plus:free` | Programming #14 | Лучшая, 1M контекст |
| Step 3.5 Flash | `stepfun/step-3.5-flash:free` | Programming #42 | Быстрая, 256K контекст |
| Nemotron 3 Super | `nvidia/nemotron-3-super:free` | Programming #7 | NVIDIA, 262K контекст |

### Telegram Bot Token
1. Открыть `@BotFather` в Telegram
2. Отправить `/newbot`
3. Вставить токен в `.env`:
   ```env
   TG_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### HH.ru API
- Бесплатно, без ключа
- Указать User-Agent в `.env`:
  ```env
  HH_USER_AGENT=CareerNavigator/1.0 (your_email@example.com)
  ```

---

## 🛠 Технологии

### Backend
| Технология | Версия | Назначение |
|------------|--------|------------|
| FastAPI | 0.115+ | REST API |
| Uvicorn | 0.30+ | ASGI сервер |
| OpenAI | 1.50+ | OpenRouter AI |
| HTTPX | 0.27+ | Асинхронные HTTP запросы |
| AioSQLite | 0.20+ | Асинхронная SQLite |
| Pydantic | 2.10+ | Валидация данных |
| python-dotenv | 1.0+ | Загрузка .env |

### Frontend
| Технология | Версия | Назначение |
|------------|--------|------------|
| React | 18.3+ | UI фреймворк |
| Vite | 5.4+ | Сборщик |
| React Router | 6.26+ | Роутинг |
| Telegram WebApp SDK | latest | Интеграция с Telegram |

### Telegram Bot
| Технология | Версия | Назначение |
|------------|--------|------------|
| python-telegram-bot | 21.6+ | Telegram Bot API |
| python-dotenv | 1.0+ | Загрузка .env |

---

## 🎨 Дизайн МТС

### Цветовая палитра
| Цвет | Код | Применение |
|------|-----|------------|
| МТС Красный | `#E30611` | Основной цвет, кнопки, акценты |
| Светлый красный | `#FF2D37` | Градиенты, hover |
| Тёмный красный | `#C4050F` | Active states |
| Красный фон | `#FFF5F5` | Фоновые элементы |
| Тёмный | `#1A1A1A` | Текст |
| Серый | `#6B7280` | Второстепенный текст |

### Особенности дизайна
- ✅ Градиенты `#E30611 → #FF2D37` на кнопках и хедерах
- ✅ Красные тени на карточках и спиннерах
- ✅ Левая красная граница на карточках вакансий и профессий
- ✅ Hover-эффекты с красным свечением
- ✅ Индикатор активной вкладки (красная точка)
- ✅ Адаптивный дизайн для мобильных

---

## 🚀 Деплой

### Backend → Railway / Render
```bash
# Railway
railway login
railway init
railway up

# Render
render deploy
```

**Environment variables:**
```
OPENROUTER_API_KEY=sk-or-v1-...
TG_BOT_TOKEN=123456789:...
HH_USER_AGENT=CareerNavigator/1.0 (email@example.com)
DATABASE_PATH=/data/career_navigator.db
```

### Frontend → Vercel / Netlify
```bash
# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

**Environment variables:**
```
VITE_API_URL=https://your-backend-url.com/api
```

### Bot → Railway / Heroku
```bash
# Railway
railway up

# Heroku
git push heroku main
```

**Environment variables:**
```
TG_BOT_TOKEN=123456789:...
FRONTEND_URL=https://your-frontend-url.com
BACKEND_URL=https://your-backend-url.com
```

---

## 📊 База данных

### Схема

```sql
-- Пользователи
users (
  telegram_id TEXT PRIMARY KEY,
  education TEXT,
  field TEXT,
  experience TEXT,
  interests TEXT,        -- JSON массив
  skills TEXT,           -- JSON массив
  career_goals TEXT,     -- JSON массив
  created_at TEXT,
  updated_at TEXT
)

-- Анализы карьеры
career_analyses (
  id INTEGER PRIMARY KEY,
  telegram_id TEXT,
  full_analysis TEXT,    -- JSON от AI
  created_at TEXT
)

-- История чата
chat_history (
  id INTEGER PRIMARY KEY,
  telegram_id TEXT,
  user_message TEXT,
  ai_response TEXT,
  context TEXT,
  created_at TEXT
)

-- Матчинг вакансий
vacancy_matches (
  id INTEGER PRIMARY KEY,
  telegram_id TEXT,
  vacancy_id INTEGER,
  profession TEXT,
  match_score REAL,
  missing_skills TEXT,   -- JSON массив
  recommendations TEXT,  -- JSON массив
  created_at TEXT
)
```

---

## 🐛 Troubleshooting

### AI возвращает демо-данные
1. Проверьте `.env` — `OPENROUTER_API_KEY` должен быть заполнен
2. Проверьте ключ: `curl -X POST https://openrouter.ai/api/v1/chat/completions -H "Authorization: Bearer YOUR_KEY" -H "Content-Type: application/json" -d '{"model":"qwen/qwen3.6-plus:free","messages":[{"role":"user","content":"test"}]}'`
3. Если Qwen rate-limited — система автоматически переключится на Step 3.5 Flash

### Frontend не подключается к backend
1. Проверьте, что backend запущен: `curl http://localhost:8000/api/health`
2. В `frontend/src/api/client.js` убедитесь, что `API_BASE` правильный
3. Проверьте CORS в `backend/main.py` (должен быть `allow_origins=["*"]`)

### Telegram бот не работает
1. Проверьте токен: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('TG_BOT_TOKEN'))"`
2. Убедитесь, что бот создан через @BotFather
3. Проверьте логи: `python bot.py` должен вывести «🤖 Бот запущен!»

### Порт 8000 занят
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

---

## 📝 TODO

- [ ] Добавить авторизацию через Telegram WebApp
- [ ] Сохранение результатов матчинга в БД
- [ ] Push-уведомления о новых вакансиях
- [ ] Экспорт резюме в PDF
- [ ] Интеграция с LinkedIn
- [ ] Мультязычность (RU/EN)
- [ ] Тёмная/светлая тема
- [ ] Unit-тесты

---

## 📄 Лицензия

MIT

---

## 👥 Контакты

- **Проект**: AI Career Navigator для МТС
- **Telegram**: @your_bot
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173

---

Made with ❤️ and AI

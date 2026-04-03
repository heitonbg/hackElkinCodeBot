# 🚀 Запуск AI Career Navigator

## 1. Установка зависимостей

### Backend
```bash
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

## 2. Настройка .env

Скопируй `.env.example` в `.env` и заполни ключи:

```bash
cp .env.example .env
```

**Обязательно:**
- `TG_BOT_TOKEN` — от @BotFather в Telegram
- `OPENROUTER_API_KEY` — бесплатно на https://openrouter.ai

## 3. Запуск

### Backend (терминал 1)
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend (терминал 2)
```bash
cd frontend
npm run dev
```

### Telegram Bot (терминал 3)
```bash
cd bot
python bot.py
```

## 4. Проверка

- Backend: http://localhost:8000/api/health
- Frontend: http://localhost:5173
- Bot: напиши /start в Telegram

## 5. Деплой (для демо)

- Backend → Railway/Render (бесплатно)
- Frontend → Vercel/Netlify (бесплатно)
- Bot → Railway/Heroku (бесплатно)

Обнови `.env` URL-адресами после деплоя!

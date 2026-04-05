"""
Telegram бот для CareerFlow.
Может запускаться отдельно или импортироваться из server.py
"""
import os
import sqlite3
import logging
import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logger = logging.getLogger(__name__)


def get_db():
    """Подключение к общей БД"""
    db_path = os.getenv("DATABASE_PATH", "/data/career_navigator.db")
    return sqlite3.connect(db_path)


async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Ежедневное напоминание — берёт пользователей из БД"""
    messages = [
        "🎭 Время для Daily Challenge! Зайди в CareerFlow и реши сегодняшнюю ситуацию!",
        "🔥 Не прерывай серию! Сегодняшняя ситуация уже ждёт тебя в CareerFlow!",
        "💪 Новый день — новый вызов! Покажи что ты знаешь — зайди и ответь на вопрос!",
        "🎯 Daily Challenge готов! Решай ситуацию в CareerFlow и зарабатывай бейджи!",
    ]

    import random
    msg = random.choice(messages)
    webapp_url = context.bot_data.get("frontend_url", "https://example.com")

    keyboard = [[InlineKeyboardButton("🚀 Решить сейчас", web_app=WebAppInfo(url=webapp_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        conn = get_db()
        cursor = conn.execute("SELECT telegram_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
    except Exception as e:
        logger.error(f"Failed to get users from DB: {e}")
        return

    if not user_ids:
        return

    sent = 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=int(uid), text=msg, reply_markup=reply_markup)
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send reminder to {uid}: {e}")

    if sent > 0:
        logger.info(f"📬 Sent daily reminders to {sent} users")


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Создаём пользователя в БД если его ещё нет"""
    uid = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name or ""
    language_code = update.effective_user.language_code or "ru"

    try:
        conn = get_db()
        cursor = conn.execute("SELECT telegram_id FROM users WHERE telegram_id = ?", (str(uid),))
        if not cursor.fetchone():
            conn.execute("""
                INSERT INTO users (telegram_id, username, first_name, last_name, language_code,
                                   education, field, experience, interests, skills, career_goals,
                                   created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, '', '', '', '[]', '[]', '[]', ?, ?)
            """, (str(uid), username, first_name, last_name, language_code,
                  datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()))
            conn.commit()
            logger.info(f"🆕 User created in DB: {uid} (@{username})")
        conn.close()
    except Exception as e:
        logger.error(f"Failed to track user {uid}: {e}")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await track_user(update, context)
    user = update.effective_user
    logger.info(f"📱 /start от {user.first_name} (id={user.id})")

    webapp_url = context.bot_data.get("webapp_url", "https://example.com")
    keyboard = [[InlineKeyboardButton("🚀 Открыть CareerFlow", web_app=WebAppInfo(url=webapp_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"Я — CareerFlow — твой персональный помощник в выборе профессии 🎯\n\n"
        f"📌 Что тебя ждёт:\n\n"
        f"🧠 Диагностика — 10 вопросов, чтобы понять твои сильные стороны\n"
        f"🎭 Тесты по ролям — 197 профессий с уникальными вопросами и ситуациями\n"
        f"📊 Результаты — подробная статистика и рекомендации\n"
        f"🔥 Daily Challenge — ежедневные ситуации для прокачки\n"
        f"🏆 Бейджи — собирай достижения за активность\n\n"
        f"Нажми кнопку ниже, чтобы начать 👇",
        reply_markup=reply_markup
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp_url = context.bot_data.get("webapp_url", "https://example.com")
    await update.message.reply_text(
        f"📖 Как пользоваться:\n\n"
        f"1. Нажми Открыть CareerFlow — перейдёшь в приложение\n"
        f"2. Пройди диагностику (10 вопросов)\n"
        f"3. Выбери интересующие роли\n"
        f"4. Пройди тестирование\n"
        f"5. Смотри результаты и вакансии\n\n"
        f"💡 Перетест доступен через 7 дней.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🚀 Открыть", web_app=WebAppInfo(url=webapp_url))
        ]])
    )


def start_bot(bot_token, webapp_url, frontend_url):
    """Запуск бота (вызывается из server.py)"""
    if not bot_token:
        logger.error("TG_BOT_TOKEN не установлен!")
        return

    logger.info(f"🤖 Бот запущен! Токен: {bot_token[:10]}...")

    app = ApplicationBuilder().token(bot_token).build()
    app.bot_data["webapp_url"] = webapp_url.rstrip('/')
    app.bot_data["frontend_url"] = frontend_url

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))

    # Ежедневная рассылка (только если job_queue доступен)
    if app.job_queue:
        app.job_queue.run_daily(daily_reminder, time=datetime.time(10, 0))

    # Запускаем polling в async режиме без обработки сигналов (для отдельного потока)
    import asyncio
    
    async def _run_polling():
        await app.initialize()
        await app.start()
        try:
            await app.updater.start_polling(drop_pending_updates=True)
            await asyncio.Event().wait()  # Блокируем навсегда
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            await app.stop()
            await app.shutdown()
    
    # Создаём новый event loop для потока
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run_polling())


def main():
    """Автономный запуск бота"""
    _env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=_env_path, override=True)

    bot_token = os.getenv("TG_BOT_TOKEN", "")
    webapp_url = os.getenv("WEBAPP_URL", "http://localhost:5173")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )

    start_bot(bot_token, webapp_url, frontend_url)


if __name__ == "__main__":
    main()

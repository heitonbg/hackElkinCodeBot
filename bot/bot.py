import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import httpx

# Загружаем .env из корня проекта
_env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Храним telegram_id пользователей (для рассылки)
known_users = set()


async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Ежедневное напоминание о Daily Challenge"""
    if not known_users:
        return

    messages = [
        "🎭 Время для Daily Challenge! Зайди в Career Navigator и реши сегодняшнюю ситуацию!",
        "🔥 Не прерывай серию! Сегодняшняя ситуация уже ждёт тебя в Career Navigator!",
        "💪 Daily Challenge готов! Покажи что ты знаешь — зайди и ответь на вопрос!",
        "🎯 Новый день — новый вызов! Решай ситуацию в Career Navigator и зарабатывай бейджи!",
    ]

    import random
    msg = random.choice(messages)

    keyboard = [[InlineKeyboardButton("🚀 Решить сейчас", url=FRONTEND_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    sent = 0
    for uid in known_users:
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=msg,
                reply_markup=reply_markup,
            )
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send reminder to {uid}: {e}")

    if sent > 0:
        logger.info(f"📬 Sent daily reminders to {sent} users")


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отслеживаем пользователя для рассылки"""
    uid = update.effective_user.id
    known_users.add(uid)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await track_user(update, context)
    user = update.effective_user
    logger.info(f"Получена команда /start от {user.first_name} (id={user.id})")

    keyboard = [
        [InlineKeyboardButton("🚀 Открыть Career Navigator", url=FRONTEND_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"Я — *AI Career Navigator* — твой персональный помощник в выборе профессии 🎯\n\n"
        f"📌 *Что тебя ждёт:*\n\n"
        f"🧠 *Диагностика* — 10 вопросов, чтобы понять твои сильные стороны\n"
        f"🎭 *Тесты по ролям* — 197 профессий с уникальными вопросами и ситуациями\n"
        f"📊 *Результаты* — подробная статистика и рекомендации\n"
        f"🔥 *Daily Challenge* — ежедневные ситуации для прокачки\n"
        f"🏆 *Бейджи* — собирай достижения за активность\n\n"
        f"Нажми кнопку ниже, чтобы начать 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        f"📖 *Как пользоваться:*\n\n"
        f"1. Нажми *🚀 Открыть Career Navigator* — перейдёшь в приложение\n"
        f"2. Пройди короткий тест (4 вопроса)\n"
        f"3. Выбери интересующие роли\n"
        f"4. Пройди тестирование\n"
        f"5. Смотри результаты и вакансии\n\n"
        f"💡 Перетест доступен через 7 дней.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🚀 Открыть", url=FRONTEND_URL)
        ]])
    )


def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.error("TG_BOT_TOKEN не установлен! Проверь .env файл.")
        print("❌ ОШИБКА: TG_BOT_TOKEN не установлен. Создай .env файл из .env.example")
        return

    logger.info(f"🤖 Бот запущен! Токен: {BOT_TOKEN[:10]}...")
    print(f"✅ Бот запущен. Frontend: {FRONTEND_URL}")
    print(f"⏰ Daily reminders enabled at 10:00 AM")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Ежедневная рассылка в 10:00
    job_queue = app.job_queue
    job_queue.run_daily(daily_reminder, hour=10, minute=0)

    app.run_polling()


if __name__ == "__main__":
    main()

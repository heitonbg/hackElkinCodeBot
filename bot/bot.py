import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    logger.info(f"Получена команда /start от {user.first_name} (id={user.id})")

    keyboard = [
        [InlineKeyboardButton("🚀 Открыть Career Navigator", url=FRONTEND_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"Я — Career Navigator, твой помощник в выборе профессии.\n\n"
        f"📌 *Что я умею:*\n"
        f"• Подберу подходящие роли по твоим навыкам\n"
        f"• Дам пройти тестирование по каждой роли\n"
        f"• Покажу реальные вакансии с HH.ru\n"
        f"• Отслежу твой прогресс и рейтинг\n\n"
        f"👇 Нажми кнопку ниже, чтобы начать:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        f"📖 *Как пользоваться:*\n\n"
        f"1. Нажми кнопку ниже или открой {FRONTEND_URL}\n"
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

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()


if __name__ == "__main__":
    main()

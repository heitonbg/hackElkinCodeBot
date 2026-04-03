import os
import logging
from dotenv import load_dotenv
from telegram import Update
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

    await update.message.reply_text(
        f"🧠 *Привет, {user.first_name}!*\n\n"
        f"Я — AI Career Navigator, твой персональный карьерный навигатор!\n\n"
        f"🎯 *Что я умею:*\n"
        f"• Анализирую твои навыки и интересы\n"
        f"• Подбираю подходящие профессии\n"
        f"• Строю карьерный путь\n"
        f"• Ищу вакансии на HH.ru\n"
        f"• Отвечаю на вопросы о карьере\n\n"
        f"📱 *Чтобы начать:*\n"
        f"1. Открой {FRONTEND_URL} в браузере\n"
        f"2. Пройди онбординг\n"
        f"3. Получи AI-рекомендации\n\n"
        f"💡 *Команды:*\n"
        f"/start — главное меню\n"
        f"/help — справка",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        f"📖 *Как пользоваться:*\n\n"
        f"1. Открой {FRONTEND_URL} в браузере\n"
        f"2. Пройди короткий онбординг\n"
        f"3. Получи персональные рекомендации\n\n"
        f"🔗 *Ссылки:*\n"
        f"• Приложение: {FRONTEND_URL}\n"
        f"• Профиль: {FRONTEND_URL}/dashboard\n"
        f"• Чат с AI: {FRONTEND_URL}/chat",
        parse_mode="Markdown"
    )


def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.error("TG_BOT_TOKEN не установлен! Проверь .env файл.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    logger.info("🤖 Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()

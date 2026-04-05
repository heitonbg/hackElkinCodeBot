"""
Unified server: запускает FastAPI + Telegram бот в одном процессе.
Запуск: cd backend && python server.py
        или: python main.py (из корня)
"""
import os
import sys
import threading
import logging
from dotenv import load_dotenv

# Загружаем .env из родительской директории
_script_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_script_dir, '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
WEBAPP_URL = os.getenv("WEBAPP_URL", FRONTEND_URL)
DATABASE_PATH = os.getenv("DATABASE_PATH")
if not DATABASE_PATH:
    # По умолчанию — корень приложения (где запускается server.py)
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "career_navigator.db")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    from bot import start_bot
    start_bot(BOT_TOKEN, WEBAPP_URL, FRONTEND_URL)


def main():
    """Запускает бот в потоке, FastAPI — в главном"""
    if not BOT_TOKEN:
        logger.error("TG_BOT_TOKEN не установлен!")
        return

    # Определяем путь к БД
    db_path = os.getenv("DATABASE_PATH")
    if not db_path:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "career_navigator.db")

    # Создаём директорию для БД (/data для облака)
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    os.environ["DATABASE_PATH"] = db_path
    logger.info(f"📦 Database path: {db_path}")

    # Запуск бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("🔄 Telegram бот запущен в фоновом потоке")

    # Добавляем backend в path
    backend_path = os.path.dirname(__file__)
    sys.path.insert(0, backend_path)

    # Запуск FastAPI
    import uvicorn
    logger.info("🚀 Запуск FastAPI сервера на порту 8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()

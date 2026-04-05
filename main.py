"""
Точка входа для деплоя (Render, Railway, Heroku и др.)
Запускает FastAPI + Telegram бот в одном процессе.

Команда запуска: python main.py
"""
import os
import sys

# Добавляем backend в path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# Импортируем и запускаем сервер
from server import main

if __name__ == "__main__":
    main()

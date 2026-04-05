"""
Сервис для валидации Telegram WebApp initData.
Основано на официальной документации Telegram:
https://core.telegram.org/bots/webapps#validating-data-from-mini-app
"""
import hmac
import hashlib
import json
import logging
from datetime import datetime
from urllib.parse import parse_qs
from typing import Optional

logger = logging.getLogger(__name__)


def validate_telegram_init_data(init_data: str, bot_token: str) -> Optional[dict]:
    """
    Валидирует initData от Telegram WebApp.
    
    Алгоритм:
    1. Парсим initData как query string
    2. Извлекаем hash
    3. Сортируем все поля кроме hash
    4. Склеиваем их в формате key=value через \n
    5. Вычисляем HMAC-SHA256 от полученной строки с ключом (HMAC-SHA256 от bot_token с сообщением "WebAppData")
    6. Сравниваем с hash из initData
    
    Возвращает распарсенные данные пользователя или None если валидация не прошла.
    """
    try:
        # Парсим initData
        parsed = parse_qs(init_data)
        
        # Преобразуем в обычный dict (parse_qs возвращает списки)
        data = {}
        for key, values in parsed.items():
            data[key] = values[0] if len(values) == 1 else values
        
        # Проверяем наличие hash
        received_hash = data.get("hash")
        if not received_hash:
            logger.warning("No hash in initData")
            return None
        
        # Проверяем auth_date (данные старше 24 часов считаем недействительными)
        auth_date = data.get("auth_date")
        if auth_date:
            auth_timestamp = int(auth_date)
            current_timestamp = int(datetime.now().timestamp())
            time_diff = current_timestamp - auth_timestamp
            # 24 часа = 86400 секунд
            if time_diff > 86400:
                logger.warning(f"initData expired: {time_diff} seconds ago")
                return None
        
        # Извлекаем hash для проверки
        check_data = data.pop("hash")
        
        # Сортируем данные по ключам
        sorted_data = sorted(data.items())
        
        # Формируем строку для проверки
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted_data)
        
        # Вычисляем секретный ключ
        secret_key = hmac.new(
            b"WebAppData",
            bot_token.encode("utf-8"),
            hashlib.sha256
        ).digest()
        
        # Вычисляем hash
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        
        # Сравниваем хеши
        if computed_hash != received_hash:
            logger.warning(f"Hash mismatch: received={received_hash[:10]}..., computed={computed_hash[:10]}...")
            return None
        
        # Валидация прошла — парсим данные пользователя
        user_data = data.get("user")
        if user_data:
            try:
                user = json.loads(user_data)
                return {
                    "id": user.get("id"),
                    "username": user.get("username"),
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "language_code": user.get("language_code"),
                    "is_premium": user.get("is_premium", False),
                    "photo_url": data.get("photo_url"),  # Может быть в initData отдельно
                }
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse user JSON: {e}")
                return None
        
        return None
        
    except Exception as e:
        logger.error(f"Telegram initData validation error: {e}")
        return None


def extract_user_from_init_data_unsafe(init_data: str) -> Optional[dict]:
    """
    Извлекает данные пользователя из initData БЕЗ валидации.
    Используется только как fallback для разработки!
    """
    try:
        parsed = parse_qs(init_data)
        data = {}
        for key, values in parsed.items():
            data[key] = values[0] if len(values) == 1 else values
        
        user_data = data.get("user")
        if user_data:
            user = json.loads(user_data)
            return {
                "id": user.get("id"),
                "username": user.get("username"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "language_code": user.get("language_code"),
                "is_premium": user.get("is_premium", False),
                "photo_url": data.get("photo_url"),
            }
        return None
    except Exception as e:
        logger.error(f"Failed to extract user from initData (unsafe): {e}")
        return None

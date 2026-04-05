"""
API endpoints для работы с Telegram WebApp.
Включает валидацию initData и управление профилем пользователя.
"""
import os
import logging
import base64
import httpx
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from services.telegram_auth import validate_telegram_init_data, extract_user_from_init_data_unsafe
from database.db import db

# Загружаем .env
_env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=_env_path, override=True)

logger = logging.getLogger(__name__)
router = APIRouter()

BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")


class TelegramAuthRequest(BaseModel):
    """Запрос на авторизацию через Telegram"""
    init_data: str
    strict_validation: bool = True  # Если False — использует unsafe режим для разработки


class TelegramUserProfile(BaseModel):
    """Профиль пользователя из Telegram"""
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    is_new_user: bool = False


@router.post("/auth", response_model=TelegramUserProfile)
async def telegram_auth(request: TelegramAuthRequest):
    """
    Авторизация пользователя через Telegram WebApp initData.

    Валидирует initData, извлекает данные пользователя и сохраняет их в БД.
    При первом входе создаёт нового пользователя.
    При повторном — обновляет Telegram-данные (username, photo, etc).
    Если strict_validation=False и initData отсутствует — создаёт demo пользователя.
    """
    user_data = None
    
    # Если есть initData — пытаемся валидировать
    if request.init_data:
        if not BOT_TOKEN:
            raise HTTPException(status_code=500, detail="TG_BOT_TOKEN not configured")
        
        user_data = validate_telegram_init_data(request.init_data, BOT_TOKEN)

        # Если строгая валидация не прошла — пробуем unsafe (для разработки)
        if not user_data and not request.strict_validation:
            logger.warning("Strict validation failed, falling back to unsafe mode")
            user_data = extract_user_from_init_data_unsafe(request.init_data)

    # Если нет initData или валидация не прошла — создаём demo пользователя (для разработки)
    if not user_data:
        if not request.strict_validation:
            logger.info("No valid initData, creating demo user for development")
            # Генерируем уникальный ID для демо пользователя
            import uuid
            telegram_id = f"demo_{uuid.uuid4().hex[:8]}"
            user_data = {
                "id": telegram_id,
                "username": "demo_user",
                "first_name": "Demo",
                "last_name": "User",
                "language_code": "ru",
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid Telegram initData")

    telegram_id = str(user_data["id"])

    # Проверяем, существует ли пользователь
    existing_user = await db.get_user(telegram_id)
    is_new_user = existing_user is None

    # Формируем данные для сохранения/обновления
    telegram_profile_data = {
        "username": user_data.get("username"),
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "photo_url": user_data.get("photo_url"),
        "language_code": user_data.get("language_code"),
    }

    if is_new_user:
        # Создаём нового пользователя с Telegram-данными
        await db.save_user(telegram_id, telegram_profile_data)
        logger.info(f"New user created: {telegram_id} (@{user_data.get('username', 'no_username')})")
    else:
        # Обновляем Telegram-данные существующего пользователя
        await db.update_telegram_profile(telegram_id, telegram_profile_data)
        logger.info(f"Updated Telegram profile for user: {telegram_id}")

    # Получаем актуальные данные пользователя
    user = await db.get_user(telegram_id)

    return TelegramUserProfile(
        telegram_id=telegram_id,
        username=user.get("username"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        photo_url=user.get("photo_url"),
        language_code=user.get("language_code"),
        is_premium=user_data.get("is_premium", False),
        is_new_user=is_new_user,
    )


@router.get("/profile/{telegram_id}", response_model=TelegramUserProfile)
async def get_telegram_profile(telegram_id: str):
    """
    Получить профиль пользователя по telegram_id.
    Возвращает все данные: Telegram + онбординг.
    """
    user = await db.get_user(telegram_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return TelegramUserProfile(
        telegram_id=str(user["telegram_id"]),
        username=user.get("username"),
        first_name=user.get("first_name"),
        last_name=user.get("last_name"),
        photo_url=user.get("photo_url"),
        language_code=user.get("language_code"),
        is_premium=False,  # Не знаем без валидации, ставим False
        is_new_user=False,
    )


@router.post("/sync-profile")
async def sync_telegram_profile(request: TelegramAuthRequest):
    """
    Синхронизировать Telegram профиль с актуальными данными.
    Полезно когда пользователь обновил username/photo в Telegram.
    """
    if not BOT_TOKEN:
        raise HTTPException(status_code=500, detail="TG_BOT_TOKEN not configured")
    
    user_data = validate_telegram_init_data(request.init_data, BOT_TOKEN)
    
    if not user_data and not request.strict_validation:
        user_data = extract_user_from_init_data_unsafe(request.init_data)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Telegram initData")
    
    telegram_id = str(user_data["id"])
    
    # Проверяем существование
    existing_user = await db.get_user(telegram_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found. Please complete onboarding first.")
    
    # Обновляем Telegram-данные
    telegram_profile_data = {
        "username": user_data.get("username"),
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "photo_url": user_data.get("photo_url"),
        "language_code": user_data.get("language_code"),
    }
    
    await db.update_telegram_profile(telegram_id, telegram_profile_data)
    
    return {
        "status": "ok",
        "telegram_id": telegram_id,
        "updated": True,
    }


@router.get("/avatar/{telegram_id}")
async def get_user_avatar(telegram_id: str):
    """
    Получить аватар пользователя как base64 изображение.
    
    Скачивает фото из Telegram Bot API и отдаёт как data URI.
    """
    if not BOT_TOKEN:
        raise HTTPException(status_code=500, detail="TG_BOT_TOKEN not configured")

    try:
        async with httpx.AsyncClient() as client:
            # 1. Получаем список фото пользователя
            resp = await client.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getUserProfilePhotos",
                params={"user_id": int(telegram_id), "limit": 1},
                timeout=10.0
            )
            data = resp.json()

        if not data.get("ok") or data.get("result", {}).get("total_count", 0) == 0:
            return {"telegram_id": telegram_id, "photo_url": None}

        # 2. Берём самое большое фото
        photo = data["result"]["photos"][0][-1]
        file_id = photo["file_id"]

        # 3. Получаем ссылку на файл
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getFile",
                params={"file_id": file_id},
                timeout=10.0
            )
            file_data = resp.json()

        if not file_data.get("ok"):
            return {"telegram_id": telegram_id, "photo_url": None}

        file_path = file_data["result"]["file_path"]
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # 4. Скачиваем фото и конвертируем в base64
        async with httpx.AsyncClient() as client:
            img_resp = await client.get(photo_url, timeout=10.0)
        
        if img_resp.status_code != 200:
            return {"telegram_id": telegram_id, "photo_url": None}

        # Определяем MIME тип
        content_type = img_resp.headers.get("content-type", "image/jpeg")
        img_base64 = base64.b64encode(img_resp.content).decode("utf-8")
        data_uri = f"data:{content_type};base64,{img_base64}"

        # 5. Сохраняем в БД
        await db.update_telegram_profile(telegram_id, {"photo_url": data_uri})

        return {"telegram_id": telegram_id, "photo_url": data_uri}

    except Exception as e:
        logger.error(f"Failed to get avatar for {telegram_id}: {e}")
        return {"telegram_id": telegram_id, "photo_url": None, "error": str(e)}

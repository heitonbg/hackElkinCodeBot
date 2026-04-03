from fastapi import APIRouter
import json
import logging
from models.models import ChatMessage
from database.db import db
from services.ai_service import chat_with_ai

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/message")
async def send_message(data: ChatMessage):
    """Отправка сообщения в AI-чат"""
    logger.info(f"Сообщение от {data.telegram_id}: {data.message[:50]}...")
    
    # Получаем историю чата для контекста
    history = await db.get_chat_history(data.telegram_id, limit=5)

    # Получаем данные пользователя для персонализации
    user = await db.get_user(data.telegram_id)
    user_context = None
    if user:
        user_context = {
            "skills": json.loads(user["skills"]) if user["skills"] else [],
            "interests": json.loads(user["interests"]) if user["interests"] else [],
            "career_goals": json.loads(user["career_goals"]) if user["career_goals"] else [],
        }

    # AI ответ
    response = await chat_with_ai(data.message, history, user_context, data.context)

    # Сохраняем в БД
    await db.save_chat_message(data.telegram_id, data.message, response, data.context)

    logger.info(f"AI ответ отправлен, длина: {len(response)} символов")
    return {"response": response}

@router.get("/history/{telegram_id}")
async def get_chat_history(telegram_id: str, limit: int = 20):
    """Получение истории чата"""
    messages = await db.get_chat_history(telegram_id, limit)
    return {"messages": messages}

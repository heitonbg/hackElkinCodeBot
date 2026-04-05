"""
API для достижений (бейджей).
"""
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from database.db import db
from services.achievement_service import get_all_achievements

logger = logging.getLogger(__name__)
router = APIRouter()


class AchievementRequest(BaseModel):
    telegram_id: str


@router.get("/list")
async def get_achievements_list(telegram_id: str):
    """Получить все бейджи + какие разблокированы"""
    all_defs = get_all_achievements()
    user_unlocked = await db.get_user_achievements(telegram_id)
    unlocked_ids = set(a["achievement_id"] for a in user_unlocked)

    result = []
    for aid, defn in all_defs.items():
        result.append({
            "achievement_id": aid,
            "emoji": defn["emoji"],
            "title": defn["title"],
            "desc": defn["desc"],
            "unlocked": aid in unlocked_ids,
            "unlocked_at": next(
                (a["unlocked_at"] for a in user_unlocked if a["achievement_id"] == aid),
                None,
            ),
        })

    return {
        "achievements": result,
        "total": len(result),
        "unlocked_count": len(unlocked_ids),
    }

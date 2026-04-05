import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Путь к файлу со сценариями
SCENARIOS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_primary.json')

class ScenarioAnswer(BaseModel):
    telegram_id: str
    role_id: str
    answers: List[dict]  # [{question_id: "sales_q1", answer: "текст ответа"}]

def load_scenarios():
    """Загружает сценарии из JSON"""
    if not os.path.exists(SCENARIOS_PATH):
        return {"scenarios": [], "error": "scenarios_primary.json не найден"}
    with open(SCENARIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.get("/scenarios")
async def get_scenarios():
    """Возвращает все сценарии для фронтенда"""
    return load_scenarios()

@router.get("/scenarios/hh")
async def get_hh_scenarios():
    """Возвращает сценарии, сгенерированные из hh.ru"""
    import json, os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_from_hh.json')

    if not os.path.exists(path):
        return {"error": "Сценарии ещё не сгенерированы. Запустите парсер."}

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.get("/scenarios/{role_id}")
async def get_scenario_by_role(role_id: str):
    """Возвращает сценарий для конкретной роли"""
    scenarios = load_scenarios()
    for s in scenarios.get("scenarios", []):
        if s.get("role_id") == role_id:
            return s
    return {"error": "Role not found"}

@router.post("/scenarios/analyze")
async def analyze_scenario_answers(data: ScenarioAnswer):
    """
    Анализирует ответы пользователя на сценарии
    Возвращает процент совпадения с ролью
    """
    from services.ai_service import analyze_scenario_match
    from database.db import db

    result = await analyze_scenario_match(data.role_id, data.answers)
    
    # Сохраняем результат в БД
    try:
        await db.save_scenario_result(data.telegram_id, data.role_id, result)
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f"Не удалось сохранить результат сценария: {e}")
    
    return result

@router.get("/leaderboard")
async def get_leaderboard(limit: int = 20):
    """Топ пользователей по результатам сценариев"""
    from database.db import db
    leaderboard = await db.get_leaderboard(limit)
    return {"leaderboard": leaderboard}

@router.get("/my-scenarios/{telegram_id}")
async def get_my_scenario_stats(telegram_id: str):
    """Статистика пользователя по сценариям"""
    from database.db import db
    stats = await db.get_user_scenario_stats(telegram_id)
    return {"results": stats}

@router.get("/all-roles")
async def get_all_roles():
    """Возвращает ВСЕ доступные роли из primary + HH сценариев"""
    import json, os

    primary_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_primary.json')
    hh_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_from_hh.json')

    roles = {}

    # Из primary
    if os.path.exists(primary_path):
        with open(primary_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for s in data.get("scenarios", []):
            rid = s["role_id"]
            roles[rid] = {
                "role_id": rid,
                "role_name": s["role_name"],
                "source": "primary",
                "question_count": len(s.get("questions", [])),
                "has_scenario": True,
            }

    # Из HH — дополняем
    if os.path.exists(hh_path):
        with open(hh_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for s in data.get("scenarios", []):
            rid = s["role_id"]
            if rid in roles:
                roles[rid]["has_hh_scenario"] = True
                roles[rid]["question_count"] += len(s.get("questions", []))
            else:
                roles[rid] = {
                    "role_id": rid,
                    "role_name": s["role_name"],
                    "source": "hh",
                    "question_count": len(s.get("questions", [])),
                    "has_scenario": True,
                    "has_hh_scenario": True,
                }

    return {"roles": list(roles.values())}

@router.get("/retest-status/{telegram_id}")
async def get_retest_status(telegram_id: str):
    """Проверить доступность перетеста"""
    from database.db import db
    status = await db.get_retest_cooldown(telegram_id)
    return status

@router.post("/retest-start/{telegram_id}")
async def start_retest(telegram_id: str):
    """Начать перетест (проверяет кулдаун)"""
    from database.db import db
    status = await db.get_retest_cooldown(telegram_id)
    if not status.get("can_retest", True):
        return {
            "can_retest": False,
            "days_remaining": status.get("days_remaining", 0),
            "next_available_date": status.get("next_available_date"),
        }
    return {"can_retest": True}

@router.post("/retest-complete/{telegram_id}")
async def complete_retest(telegram_id: str):
    """Завершить перетест — установить кулдаун 7 дней"""
    from database.db import db
    await db.set_retest_cooldown(telegram_id, days=7)
    return {"status": "cooldown_set", "next_available_days": 7}

@router.post("/scenarios/save-answers")
async def save_scenario_answers(data: ScenarioAnswer):
    """Сохранить сырые ответы (без анализа) — для последующей обработки"""
    from database.db import db
    await db.save_scenario_answers(data.telegram_id, data.role_id, data.answers)
    return {"status": "saved", "role_id": data.role_id}

@router.post("/scenarios/analyze-pending/{telegram_id}")
async def analyze_pending(telegram_id: str):
    """Анализировать один pending ответ, сохранить результат, удалить сырые"""
    from database.db import db
    from services.ai_service import analyze_scenario_match

    pending = await db.get_pending_scenario_answers(telegram_id)
    if not pending:
        return {"status": "no_pending", "result": None}

    item = pending[0]  # Берём первый
    result = await analyze_scenario_match(item["role_id"], item["answers"])

    # Сохраняем результат
    await db.save_scenario_result(telegram_id, item["role_id"], result)
    # Удаляем сырые
    await db.delete_scenario_answers(telegram_id)

    return {"status": "done", "role_id": item["role_id"], "result": result}

@router.get("/scenarios/pending-count/{telegram_id}")
async def pending_count(telegram_id: str):
    """Сколько ответов ждут анализа"""
    from database.db import db
    pending = await db.get_pending_scenario_answers(telegram_id)
    return {"count": len(pending), "roles": [p["role_id"] for p in pending]}

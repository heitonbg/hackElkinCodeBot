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
    with open(SCENARIOS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

@router.get("/scenarios")
async def get_scenarios():
    """Возвращает все сценарии для фронтенда"""
    return load_scenarios()

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
    
    result = await analyze_scenario_match(data.role_id, data.answers)
    return result

@router.get("/scenarios/hh")
async def get_hh_scenarios():
    """Возвращает сценарии, сгенерированные из hh.ru"""
    import json, os
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scenarios_from_hh.json')
    
    if not os.path.exists(path):
        return {"error": "Сценарии ещё не сгенерированы. Запустите парсер."}
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)
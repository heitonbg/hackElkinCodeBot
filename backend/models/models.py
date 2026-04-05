from pydantic import BaseModel
from typing import Optional, List

class UserProfile(BaseModel):
    telegram_id: str
    education: Optional[str] = None
    field: Optional[str] = None
    experience: Optional[str] = None
    interests: list[str] = []
    skills: list[str] = []
    career_goals: list[str] = []

class OnboardingData(BaseModel):
    telegram_id: str
    education: Optional[str] = None
    field: Optional[str] = None
    experience: Optional[str] = None
    interests: list[str] = []
    skills: list[str] = []
    career_goals: list[str] = []

class CareerAnalysis(BaseModel):
    telegram_id: str

class VacancyFilter(BaseModel):
    telegram_id: str
    profession: Optional[str] = None
    location: Optional[str] = None

class ChatMessage(BaseModel):
    telegram_id: str
    message: str
    context: Optional[str] = None

# Новые модели для AI-генерации
class RoleGenerationRequest(BaseModel):
    telegram_id: str

class ScenarioGenerationRequest(BaseModel):
    telegram_id: str
    role_id: str
    role_data: dict = {}  # title, match_percent, reason, key_skills и т.д.

class ScenarioAnswer(BaseModel):
    telegram_id: str
    role_id: str
    answers: List[dict]  # [{question_id: "...", answer: "..."}]

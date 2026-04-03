from pydantic import BaseModel
from typing import Optional

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

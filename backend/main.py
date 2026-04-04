import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import user, career, vacancies, chat, scenarios, roles, onboarding
from database.db import db

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Career Navigator API",
    description="API для AI-карьерного навигатора",
    version="1.0.0"
)

# CORS для React Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к БД при старте
@app.on_event("startup")
async def startup():
    logger.info("🚀 Запуск AI Career Navigator API...")
    await db.init_db()
    logger.info("✅ База данных инициализирована")

# Маршруты
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(career.router, prefix="/api/career", tags=["Career"])
app.include_router(vacancies.router, prefix="/api/vacancies", tags=["Vacancies"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(scenarios.router, prefix="/api/scenarios", tags=["Scenarios"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])
app.include_router(onboarding.router, prefix="/api/onboarding", tags=["Onboarding"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "AI Career Navigator"}

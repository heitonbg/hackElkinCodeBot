import aiosqlite
import os
import json
from datetime import datetime

DATABASE_PATH = os.getenv("DATABASE_PATH", "career_navigator.db")

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Таблица пользователей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id TEXT PRIMARY KEY,
                    education TEXT,
                    field TEXT,
                    experience TEXT,
                    interests TEXT,
                    skills TEXT,
                    career_goals TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # Таблица анализов карьеры — храним полный JSON от AI
            await db.execute("""
                CREATE TABLE IF NOT EXISTS career_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    full_analysis TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)
            
            # Таблица матчинга вакансий
            await db.execute("""
                CREATE TABLE IF NOT EXISTS vacancy_matches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    vacancy_id INTEGER,
                    profession TEXT,
                    match_score REAL,
                    missing_skills TEXT,
                    recommendations TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)
            
            # Таблица истории чата
            await db.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    user_message TEXT,
                    ai_response TEXT,
                    context TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)
            
            await db.commit()

    async def save_user(self, telegram_id: str, data: dict):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users
                (telegram_id, education, field, experience, interests, skills, career_goals, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?,
                    COALESCE((SELECT created_at FROM users WHERE telegram_id = ?), ?),
                    ?)
            """, (
                telegram_id,
                data.get("education"),
                data.get("field"),
                data.get("experience"),
                json.dumps(data.get("interests", [])),
                json.dumps(data.get("skills", [])),
                json.dumps(data.get("career_goals", [])),
                telegram_id,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            await db.commit()

    async def get_user(self, telegram_id: str) -> dict:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))

    async def save_analysis(self, telegram_id: str, analysis: dict):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO career_analyses (telegram_id, full_analysis, created_at)
                VALUES (?, ?, ?)
            """, (
                telegram_id,
                json.dumps(analysis, ensure_ascii=False),
                datetime.now().isoformat()
            ))
            await db.commit()

    async def save_chat_message(self, telegram_id: str, user_msg: str, ai_resp: str, context: str = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO chat_history (telegram_id, user_message, ai_response, context, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, user_msg, ai_resp, context, datetime.now().isoformat()))
            await db.commit()

    async def get_chat_history(self, telegram_id: str, limit: int = 20):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT user_message, ai_response FROM chat_history WHERE telegram_id = ? ORDER BY id DESC LIMIT ?",
                (telegram_id, limit)
            ) as cursor:
                rows = await cursor.fetchall()
                return [{"user_message": r[0], "ai_response": r[1]} for r in reversed(rows)]

    async def get_latest_analysis(self, telegram_id: str):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT full_analysis, created_at FROM career_analyses WHERE telegram_id = ? ORDER BY id DESC LIMIT 1",
                (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                analysis = json.loads(row[0]) if row[0] else {}
                analysis["created_at"] = row[1]
                return analysis

db = Database()

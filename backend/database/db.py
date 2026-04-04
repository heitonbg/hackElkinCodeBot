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

            # Таблица результатов сценариев
            await db.execute("""
                CREATE TABLE IF NOT EXISTS scenario_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    role_id TEXT,
                    match_score REAL,
                    strengths TEXT,
                    weaknesses TEXT,
                    feedback TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)

            # Таблица кулдауна перетеста
            await db.execute("""
                CREATE TABLE IF NOT EXISTS retest_cooldowns (
                    telegram_id TEXT PRIMARY KEY,
                    last_test_date TEXT,
                    next_available_date TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)

            # Таблица сырых ответов сценариев (ждут анализа)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS scenario_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    role_id TEXT,
                    answers TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)

            # Таблица AI-сгенерированных сценариев
            await db.execute("""
                CREATE TABLE IF NOT EXISTS generated_scenarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    role_id TEXT,
                    scenario_json TEXT,
                    created_at TEXT,
                    FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
                )
            """)

            # Таблица AI-анализов результатов сценариев
            await db.execute("""
                CREATE TABLE IF NOT EXISTS ai_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id TEXT,
                    role_id TEXT,
                    analysis_json TEXT,
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

    async def save_scenario_result(self, telegram_id: str, role_id: str, result: dict):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO scenario_results (telegram_id, role_id, match_score, strengths, weaknesses, feedback, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                telegram_id,
                role_id,
                result.get("match_score", 0),
                json.dumps(result.get("strengths", []), ensure_ascii=False),
                json.dumps(result.get("weaknesses", []), ensure_ascii=False),
                result.get("feedback", ""),
                datetime.now().isoformat()
            ))
            await db.commit()

    async def get_leaderboard(self, limit: int = 20):
        """Топ пользователей по среднему match_score"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT telegram_id, 
                       ROUND(AVG(match_score), 1) as avg_score,
                       COUNT(*) as scenarios_completed
                FROM scenario_results
                GROUP BY telegram_id
                ORDER BY avg_score DESC
                LIMIT ?
            """, (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        "telegram_id": r[0],
                        "avg_score": r[1],
                        "scenarios_completed": r[2]
                    }
                    for r in rows
                ]

    async def get_user_scenario_stats(self, telegram_id: str):
        """Статистика пользователя по сценариям"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT role_id, match_score, feedback, created_at
                FROM scenario_results
                WHERE telegram_id = ?
                ORDER BY created_at DESC
            """, (telegram_id,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {
                        "role_id": r[0],
                        "match_score": r[1],
                        "feedback": r[2],
                        "created_at": r[3]
                    }
                    for r in rows
                ]

    async def set_retest_cooldown(self, telegram_id: str, days: int = 7):
        """Установить кулдаун перетеста"""
        from datetime import datetime, timedelta
        now = datetime.now()
        next_date = now + timedelta(days=days)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO retest_cooldowns (telegram_id, last_test_date, next_available_date)
                VALUES (?, ?, ?)
            """, (telegram_id, now.isoformat(), next_date.isoformat()))
            await db.commit()

    async def get_retest_cooldown(self, telegram_id: str):
        """Проверить доступность перетеста"""
        from datetime import datetime
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT last_test_date, next_available_date
                FROM retest_cooldowns
                WHERE telegram_id = ?
            """, (telegram_id,)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return {"can_retest": True}
                now = datetime.now()
                next_date = datetime.fromisoformat(row[1])
                return {
                    "can_retest": now >= next_date,
                    "last_test_date": row[0],
                    "next_available_date": row[1],
                    "days_remaining": max(0, (next_date - now).days),
                }

    async def save_scenario_answers(self, telegram_id: str, role_id: str, answers: list):
        """Сохранить сырые ответы сценария (для последующего анализа)"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO scenario_answers (telegram_id, role_id, answers, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                telegram_id,
                role_id,
                json.dumps(answers, ensure_ascii=False),
                datetime.now().isoformat()
            ))
            await db.commit()

    async def get_pending_scenario_answers(self, telegram_id: str):
        """Получить неотанализированные ответы"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT id, role_id, answers
                FROM scenario_answers
                WHERE telegram_id = ?
                ORDER BY id ASC
            """, (telegram_id,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    {"id": r[0], "role_id": r[1], "answers": json.loads(r[2])}
                    for r in rows
                ]

    async def delete_scenario_answers(self, telegram_id: str):
        """Удалить сырые ответы после анализа"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM scenario_answers WHERE telegram_id = ?", (telegram_id,))
            await db.commit()

    async def save_generated_scenario(self, telegram_id: str, role_id: str, scenario: dict):
        """Сохранить AI-сгенерированный сценарий"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO generated_scenarios (telegram_id, role_id, scenario_json, created_at)
                VALUES (?, ?, ?, ?)
            """, (
                telegram_id,
                role_id,
                json.dumps(scenario, ensure_ascii=False),
                datetime.now().isoformat()
            ))
            await db.commit()

    async def get_generated_scenario(self, telegram_id: str, role_id: str):
        """Получить AI-сгенерированный сценарий"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT scenario_json, created_at
                FROM generated_scenarios
                WHERE telegram_id = ? AND role_id = ?
                ORDER BY id DESC LIMIT 1
            """, (telegram_id, role_id)) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                scenario = json.loads(row[0]) if row[0] else {}
                scenario["created_at"] = row[1]
                return scenario

    async def save_ai_analysis(self, telegram_id: str, role_id: str, analysis: dict):
        """Сохранить AI-анализ результатов сценария"""
        async with aiosqlite.connect(self.db_path) as db:
            # Проверяем, есть ли уже анализ
            async with db.execute("""
                SELECT id FROM ai_analyses WHERE telegram_id = ? AND role_id = ?
                ORDER BY id DESC LIMIT 1
            """, (telegram_id, role_id)) as cursor:
                existing = await cursor.fetchone()

            if existing:
                await db.execute("""
                    UPDATE ai_analyses SET analysis_json = ?, created_at = ?
                    WHERE id = ?
                """, (json.dumps(analysis, ensure_ascii=False), datetime.now().isoformat(), existing[0]))
            else:
                await db.execute("""
                    INSERT INTO ai_analyses (telegram_id, role_id, analysis_json, created_at)
                    VALUES (?, ?, ?, ?)
                """, (telegram_id, role_id, json.dumps(analysis, ensure_ascii=False), datetime.now().isoformat()))
            await db.commit()

    async def get_ai_analysis(self, telegram_id: str, role_id: str = None):
        """Получить AI-анализ для пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            if role_id:
                async with db.execute("""
                    SELECT analysis_json, created_at
                    FROM ai_analyses
                    WHERE telegram_id = ? AND role_id = ?
                    ORDER BY id DESC LIMIT 1
                """, (telegram_id, role_id)) as cursor:
                    row = await cursor.fetchone()
                    if not row:
                        return None
                    analysis = json.loads(row[0]) if row[0] else {}
                    analysis["created_at"] = row[1]
                    return analysis
            else:
                async with db.execute("""
                    SELECT role_id, analysis_json, created_at
                    FROM ai_analyses
                    WHERE telegram_id = ?
                    ORDER BY id DESC
                """, (telegram_id,)) as cursor:
                    rows = await cursor.fetchall()
                    result = []
                    for r in rows:
                        item = json.loads(r[1]) if r[1] else {}
                        item["role_id"] = r[0]
                        item["created_at"] = r[2]
                        result.append(item)
                    return result

db = Database()

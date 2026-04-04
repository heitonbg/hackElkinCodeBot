"""
Генератор базы профессий. Запуск: python backend/scripts/generate_roles_db.py
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.roles_data import PROFESSIONS, SCENARIO_TEMPLATES

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'roles_database.json')

def generate():
    roles = []
    for cat_id, cat_data in PROFESSIONS.items():
        templates = SCENARIO_TEMPLATES.get(cat_id, SCENARIO_TEMPLATES["default"])
        for role in cat_data["roles"]:
            jq = [{"id": f"{role['id']}_j_q{i+1}", "text": q["q"], "options": q["options"], "level": "junior"}
                  for i, q in enumerate(templates["junior"])]
            mq = [{"id": f"{role['id']}_m_q{i+1}", "text": q["q"], "options": q["options"], "level": "middle"}
                  for i, q in enumerate(templates["middle"])]
            roles.append({
                "role_id": role["id"],
                "title": role["title"],
                "category": cat_data["name"],
                "category_id": cat_id,
                "skills": role["skills"],
                "salary": {"junior": role["salary_junior"], "middle": role["salary_middle"]},
                "scenarios": {
                    "junior": {"level": "junior", "description": f"Базовый уровень для {role['title']}", "questions": jq},
                    "middle": {"level": "middle", "description": f"Продвинутый уровень для {role['title']}", "questions": mq},
                }
            })
    db = {"version": "1.0", "total_roles": len(roles), "roles": roles}
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    tq = sum(len(r["scenarios"]["junior"]["questions"]) + len(r["scenarios"]["middle"]["questions"]) for r in roles)
    print(f"✅ roles_database.json — {len(roles)} ролей, {tq} вопросов, {os.path.getsize(OUTPUT_PATH)/1024:.0f} KB")

if __name__ == "__main__":
    generate()

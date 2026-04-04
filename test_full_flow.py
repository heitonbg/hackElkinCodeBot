import httpx
import asyncio
import json

async def setup_and_test():
    async with httpx.AsyncClient(timeout=30) as c:
        # Сначала создадим пользователя через онбординг
        print("1. Создаю пользователя...")
        onboard_data = {
            "telegram_id": "demo_user",
            "education": "Бакалавриат",
            "field": "Python-разработчик",
            "experience": "Нет опыта (ищу первую работу / стажировку)",
            "interests": ["IT и разработка", "Аналитика данных"],
            "skills": ["Python", "SQL", "Excel"],
            "career_goals": ["Найти первую работу"],
        }
        r = await c.post('http://localhost:8000/api/user/onboarding', json=onboard_data)
        print(f"   Onboarding: {r.status_code} - {r.text[:200]}")

        # Профиль
        print("\n2. Профиль...")
        r = await c.get('http://localhost:8000/api/user/profile/demo_user')
        d = r.json()
        print(f"   Exists: {d.get('exists')}")
        if d.get('profile'):
            print(f"   Field: {d['profile'].get('field')}")
            print(f"   Skills: {d['profile'].get('skills')}")

        # Рекомендации
        print("\n3. Рекомендации...")
        r = await c.get('http://localhost:8000/api/career/recommendations/demo_user')
        print(f"   Status: {r.status_code}")
        d = r.json()
        if d.get('error'):
            print(f"   ОШИБКА: {d['error']}")
        elif d.get('top_skills_to_develop'):
            print(f"   OK! {len(d['top_skills_to_develop'])} рекомендаций")
            for s in d['top_skills_to_develop']:
                print(f"   - {s['skill']} ({s['priority']})")
                print(f"     Почему: {s['why']}")
                print(f"     Как: {s['how_to_learn']}")
        else:
            print(f"   Ответ: {json.dumps(d, indent=2)[:300]}")

asyncio.run(setup_and_test())

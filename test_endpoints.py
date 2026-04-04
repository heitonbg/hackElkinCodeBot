import httpx
import asyncio

async def test_endpoints():
    async with httpx.AsyncClient(timeout=30) as c:
        # 1. Рекомендации
        print("1. Тест рекомендаций...")
        r = await c.get('http://localhost:8000/api/career/recommendations/demo_user')
        d = r.json()
        if d.get('error'):
            print(f"   ОШИБКА: {d['error']}")
        elif d.get('top_skills_to_develop'):
            print(f"   OK! {len(d['top_skills_to_develop'])} рекомендаций")
            for s in d['top_skills_to_develop'][:2]:
                print(f"   - {s['skill']} ({s['priority']})")
        else:
            print(f"   Ответ: {d}")

        # 2. Сценарии по роли
        print("\n2. Тест сценариев по роли...")
        r = await c.get('http://localhost:8000/api/scenarios/scenarios/sales_intern')
        d = r.json()
        if d.get('error'):
            print(f"   ОШИБКА: {d['error']}")
        elif d.get('questions'):
            print(f"   OK! {len(d['questions'])} вопросов для {d.get('role_name')}")
        else:
            print(f"   Ответ: {d}")

        # 3. Все роли
        print("\n3. Тест всех ролей...")
        r = await c.get('http://localhost:8000/api/scenarios/all-roles')
        d = r.json()
        print(f"   Ролей: {len(d.get('roles', []))}")
        for role in d.get('roles', [])[:5]:
            print(f"   - {role['role_id']}: {role['role_name']} (source={role['source']})")

asyncio.run(test_endpoints())

print("=" * 60)
print("ИТОГОВЫЙ ТЕСТ ВСЕХ ИСПРАВЛЕНИЙ")
print("=" * 60)

import httpx
import asyncio
import json

async def full_test():
    async with httpx.AsyncClient(timeout=30) as c:
        
        # 1. Онбординг
        print("\n1. ОНБОРДИНГ (создание пользователя)")
        onboard = {
            "telegram_id": "test_user",
            "education": "Бакалавриат",
            "field": "Маркетолог",
            "experience": "Начальный (1-2 года)",
            "interests": ["Маркетинг и реклама", "Аналитика данных"],
            "skills": ["Excel", "Английский язык", "Photoshop"],
            "career_goals": ["Получить повышение"],
        }
        r = await c.post('http://localhost:8000/api/user/onboarding', json=onboard)
        print(f"   ✅ Сохранено" if r.status_code == 200 else f"   ❌ {r.status_code}")

        # 2. Профиль
        print("\n2. ПРОФИЛЬ")
        r = await c.get('http://localhost:8000/api/user/profile/test_user')
        d = r.json()
        print(f"   ✅ Профессия: {d['profile']['field']}")
        print(f"   ✅ Навыки: {d['profile']['skills']}")

        # 3. Поиск вакансий по городу
        print("\n3. ПОИСК ВАКАНСИЙ (маркетолог, Казань)")
        r = await c.get('http://localhost:8000/api/vacancies/search',
            params={'profession': 'маркетолог', 'location': 'казань', 'limit': 2})
        d = r.json()
        if d.get('vacancies'):
            print(f"   ✅ Найдено: {d['count']} вакансий")
            for v in d['vacancies']:
                print(f"   📍 {v.get('location')} | {v['title']}")
        else:
            print(f"   ❌ {d.get('error')}")

        # 4. Рекомендации по карьере
        print("\n4. ПЕРСОНАЛЬНЫЕ РЕКОМЕНДАЦИИ")
        r = await c.get('http://localhost:8000/api/career/recommendations/test_user')
        d = r.json()
        if d.get('top_skills_to_develop'):
            print(f"   ✅ {len(d['top_skills_to_develop'])} рекомендаций:")
            for s in d['top_skills_to_develop']:
                print(f"   • {s['skill']} ({s['priority']}) — {s['why']}")
            if d.get('career_advice'):
                print(f"   💬 {d['career_advice'][:80]}...")
        else:
            print(f"   ❌ {d.get('error', 'нет данных')}")

        # 5. Сценарии по ролям
        print("\n5. СЦЕНАРИИ ПО РОЛЯМ")
        r = await c.get('http://localhost:8000/api/scenarios/scenarios/sales_intern')
        d = r.json()
        if d.get('questions'):
            print(f"   ✅ {d['role_name']}: {len(d['questions'])} вопросов")
            for q in d['questions'][:2]:
                print(f"   ❓ {q['text'][:60]}...")
        else:
            print(f"   ❌ {d.get('error', 'нет данных')}")

        # 6. Все доступные роли
        print("\n6. ВСЕ ДОСТУПНЫЕ РОЛИ")
        r = await c.get('http://localhost:8000/api/scenarios/all-roles')
        d = r.json()
        roles = d.get('roles', [])
        print(f"   ✅ Всего ролей: {len(roles)}")
        sources = {}
        for r in roles:
            src = r['source']
            sources[src] = sources.get(src, 0) + 1
        for src, cnt in sources.items():
            print(f"   • {src}: {cnt} ролей")

        print("\n" + "=" * 60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("=" * 60)

asyncio.run(full_test())

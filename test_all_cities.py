import httpx
import asyncio

async def test_cities():
    cities = ['москва', 'казань', 'екатеринбург', 'новосибирск', 'питер']
    async with httpx.AsyncClient(timeout=30) as c:
        for city in cities:
            r = await c.get('http://localhost:8000/api/vacancies/search',
                params={'profession': 'python', 'location': city, 'limit': 2})
            d = r.json()
            print(f"\n{city.upper()}: {d.get('count', 0)} вакансий")
            for v in d.get('vacancies', [])[:2]:
                print(f"  📍 {v.get('location')} | {v['title']} @ {v['company']}")

asyncio.run(test_cities())

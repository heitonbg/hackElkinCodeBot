import httpx
import asyncio

async def test_city():
    async with httpx.AsyncClient(timeout=30) as client:
        # Тест с городом
        resp = await client.get(
            "http://localhost:8000/api/vacancies/search",
            params={"profession": "python", "location": "казань", "limit": 3}
        )
        data = resp.json()
        print(f"Казань: {data.get('count', 0)} вакансий, source={data.get('source')}")
        if data.get('vacancies'):
            for v in data['vacancies']:
                print(f"  - {v['title']} @ {v['company']}, location={v.get('location')}")
        if data.get('error'):
            print(f"  ОШИБКА: {data['error']}")

asyncio.run(test_city())

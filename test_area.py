import httpx
import asyncio

async def test_hh_area():
    async with httpx.AsyncClient(timeout=10) as c:
        # С area
        r = await c.get('https://api.hh.ru/vacancies', params={
            'text': 'python',
            'area': '11',
            'per_page': 3
        })
        d = r.json()
        print(f"С area=11: Found={d.get('found',0)}")
        for i in d.get('items', []):
            area = i.get('area', {})
            print(f"  {i['name']} -> {area.get('name', 'N/A')}")

asyncio.run(test_hh_area())

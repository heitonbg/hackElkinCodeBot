import httpx
import asyncio

async def test_recs():
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.get('http://localhost:8000/api/career/recommendations/demo_user')
        print(f"Status: {r.status_code}")
        print(f"Content: {r.text[:500]}")

asyncio.run(test_recs())

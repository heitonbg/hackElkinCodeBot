import httpx
import asyncio

async def test_direct_hh():
    print("Testing direct HH.ru API...")
    async with httpx.AsyncClient(timeout=15) as client:
        try:
            response = await client.get(
                "https://api.hh.ru/vacancies",
                params={
                    "text": "python",
                    "per_page": 3
                },
                headers={"User-Agent": "CareerNavigator/1.0 (career-navigator@example.com)"}
            )
            print(f"HH.ru Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Found {data.get('found', 0)} vacancies")
                print(f"Items count: {len(data.get('items', []))}")
                if data.get('items'):
                    first = data['items'][0]
                    print(f"First vacancy: {first.get('name')}")
                    print(f"Has key_skills: {'key_skills' in first}")
            else:
                print(f"Error response: {response.text[:200]}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_direct_hh())

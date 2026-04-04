import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            'http://localhost:8000/api/vacancies/search',
            params={
                'profession': 'python',
                'location': 'москва',
                'limit': 3
            }
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Count: {data.get('count', 0)}")
        print(f"Source: {data.get('source', 'unknown')}")
        
        if data.get('vacancies'):
            print(f"\nНайдено {len(data['vacancies'])} вакансий:")
            for i, v in enumerate(data['vacancies'][:3], 1):
                print(f"\n{i}. {v.get('title')}")
                print(f"   Компания: {v.get('company')}")
                print(f"   Зарплата: {v.get('salary')}")
                print(f"   Requirements: {len(v.get('requirements', []))}")
                if v.get('requirements'):
                    print(f"   Первые 3: {v['requirements'][:3]}")
        else:
            print("No vacancies found")
            if data.get('error'):
                print(f"Error: {data['error']}")

if __name__ == "__main__":
    asyncio.run(test_api())

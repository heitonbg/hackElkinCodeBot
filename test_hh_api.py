import httpx
import asyncio

async def test_hh_search():
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
            print(f"\nFirst vacancy:")
            v = data['vacancies'][0]
            print(f"  Title: {v.get('title')}")
            print(f"  Company: {v.get('company')}")
            print(f"  Salary: {v.get('salary')}")
            print(f"  Requirements count: {len(v.get('requirements', []))}")
            if v.get('requirements'):
                print(f"  First 3 requirements: {v['requirements'][:3]}")
        else:
            print("No vacancies found")
            if data.get('error'):
                print(f"Error: {data['error']}")

if __name__ == "__main__":
    asyncio.run(test_hh_search())

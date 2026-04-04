import httpx
import asyncio
import time

async def test_hh_speed():
    print("=== ЗАМЕР СКОРОСТИ ПОИСКА ВАКАНСИЙ ===\n")
    
    # 1. Тест напрямую к HH.ru
    print("1. Прямой запрос к HH.ru API...")
    t0 = time.time()
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(
            "https://api.hh.ru/vacancies",
            params={"text": "python", "per_page": 10},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
    t1 = time.time()
    print(f"   HH.ru ответ: {t1-t0:.2f} сек, найдено: {resp.json().get('found', 0)}")
    
    # 2. Тест через backend сервис
    print("\n2. Через backend сервис (с деталями)...")
    import sys
    sys.path.insert(0, 'backend')
    t0 = time.time()
    from services.hh_service import search_vacancies
    vacancies = await search_vacancies("python", "", 10)
    t1 = time.time()
    print(f"   Backend ответ: {t1-t0:.2f} сек, вакансий: {len(vacancies)}")
    if vacancies:
        v = vacancies[0]
        print(f"   Первая: {v['title']} @ {v['company']}")
        print(f"   Requirements: {len(v.get('requirements', []))}")
    
    # 3. Тест через API endpoint
    print("\n3. Через API endpoint (HTTP)...")
    t0 = time.time()
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            "http://localhost:8000/api/vacancies/search",
            params={"profession": "python", "limit": 10}
        )
    t1 = time.time()
    print(f"   API ответ: {t1-t0:.2f} сек, статус: {resp.status_code}")
    data = resp.json()
    print(f"   Вакансий: {data.get('count', 0)}, source: {data.get('source')}")
    if data.get('error'):
        print(f"   ОШИБКА: {data['error']}")
    
    print(f"\n=== ИТОГО ===")

if __name__ == "__main__":
    asyncio.run(test_hh_speed())

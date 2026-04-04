import httpx
import asyncio
import sys
import os

# Добавляем backend в path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_hh_service():
    print("Тестирую hh_service напрямую...")
    from services.hh_service import search_vacancies
    
    try:
        vacancies = await search_vacancies("python", "москва", 3)
        print(f"Найдено вакансий: {len(vacancies)}")
        if vacancies:
            v = vacancies[0]
            print(f"Первая вакансия: {v.get('title')}")
            print(f"Компания: {v.get('company')}")
            print(f"Зарплата: {v.get('salary')}")
            print(f"Requirements: {len(v.get('requirements', []))}")
            if v.get('requirements'):
                print(f"Первые 3 требования: {v['requirements'][:3]}")
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_hh_service())

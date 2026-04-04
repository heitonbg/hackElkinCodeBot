import httpx
import asyncio

async def get_correct_areas():
    """Найти правильные area_id для городов"""
    cities = ['казань', 'москва', 'санкт-петербург', 'новосибирск', 'екатеринбург']
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get('https://api.hh.ru/areas')
        areas = r.json()
        
        for city in cities:
            # Рекурсивный поиск
            for area in areas:
                for a2 in area.get('areas', []):
                    for a3 in a2.get('areas', []):
                        if city in a3.get('name', '').lower():
                            print(f"{city} -> id={a3['id']} (area)")
                    for city_item in a2.get('cities', []):
                        if city in city_item.get('name', '').lower():
                            print(f"{city} -> id={city_item['id']} (city)")
                for city_item in area.get('cities', []):
                    if city in city_item.get('name', '').lower():
                        print(f"{city} -> id={city_item['id']} (city)")

asyncio.run(get_correct_areas())

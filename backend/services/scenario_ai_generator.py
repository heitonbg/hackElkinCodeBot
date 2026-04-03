import asyncio
import json
import os
from services.ai_service import _call_openai_with_fallback

async def generate_scenario_with_ai(requirement: str, role_name: str) -> dict:
    """Генерирует качественный сценарий через AI"""
    
    prompt = f"""
Ты — эксперт по найму. Придумай реалистичный сценарий-вопрос для проверки навыка.

Роль: {role_name}
Навык/требование: "{requirement}"

Придумай:
1. Ситуацию (1-2 предложения)
2. 4 варианта ответа (A, B, C, D), где:
   - A — плохой ответ
   - B — неплохой, но не идеальный
   - C — хороший ответ
   - D — ? придумай сам
   - E - "Свой вариант", так и оставь.

Верни ТОЛЬКО JSON:
{{
    "question": "текст ситуации и вопроса",
    "options": ["Вариант A", "Вариант B", "Вариант C", "Свой вариант"]
}}
"""
    try:
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — HR-эксперт. Отвечай строго JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800
        )
        content = content.strip().strip("```json").strip("```").strip()
        return json.loads(content)
    except Exception as e:
        print(f"AI ошибка: {e}")
        # Возвращаем базовый сценарий
        return {
            "question": f"Как бы ты применил навык: {requirement[:100]}?",
            "options": ["Расскажу про опыт", "Покажу сертификат", "Сделаю тестовое задание", "Свой вариант"]
        }


async def generate_all_scenarios_with_ai():
    """Генерирует сценарии для всех ролей через AI"""
    # Загружаем требования
    current_dir = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.join(current_dir, '..', 'data', 'hh_requirements.json')
    
    with open(req_path, 'r', encoding='utf-8') as f:
        requirements_data = json.load(f)
    
    all_scenarios = []
    
    for role_id, role_data in requirements_data.items():
        if "error" in role_data:
            continue
        
        role_name = role_data.get("role_name", role_id)
        requirements = role_data.get("requirements", [])
        
        print(f"🎯 Генерирую сценарии для {role_name}...")
        
        role_scenarios = []
        for req in requirements[:5]:  # Берём топ-5 требований
            req_text = req.get("text", "")
            if req_text and len(req_text) > 10:
                scenario = await generate_scenario_with_ai(req_text, role_name)
                role_scenarios.append({
                    "id": f"{role_id}_q{len(role_scenarios)+1}",
                    "text": scenario.get("question", ""),
                    "options": scenario.get("options", [])
                })
        
        if role_scenarios:
            all_scenarios.append({
                "role_id": role_id,
                "role_name": role_name.replace("_", " ").title(),
                "questions": role_scenarios
            })
    
    # Сохраняем
    data_dir = os.path.join(current_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, 'scenarios_ai_generated.json')
    
    output = {
        "total_roles": len(all_scenarios),
        "generated_by": "AI",
        "scenarios": all_scenarios
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Сгенерировано {len(all_scenarios)} ролей, сохранено в {out_path}")
    return output


if __name__ == "__main__":
    asyncio.run(generate_all_scenarios_with_ai())
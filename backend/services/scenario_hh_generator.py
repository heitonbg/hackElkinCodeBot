"""
Генератор качественных сценариев из hh_requirements.json
Использует AI для создания релевантных вопросов на основе НАВЫКОВ (skills), а не сырых требований
"""
import asyncio
import json
import os
from services.ai_service import _call_openai_with_fallback


# Маппинг ролей HH -> role_id в МТС
ROLE_MAPPING = {
    "sales": "sales_intern",
    "hr": "hr_intern",
    "python_dev": "ai_analyst",  # Python dev -> AI аналитик
    "data_analyst": "ai_analyst",
    "marketing": "marketing",
    "lawyer": "lawyer",
    "procurement": "procurement",
    "engineer": "engineer_lks",
    "seller": "seller",
}

# Человекочитаемые названия
ROLE_NAMES = {
    "sales_intern": "Стажер направление продаж и развития",
    "hr_intern": "Стажер HR",
    "ai_analyst": "Аналитик по внедрению AI",
    "marketing": "Маркетинг",
    "lawyer": "Юрист",
    "procurement": "Специалист по сопровождению закупок",
    "engineer_lks": "Стажёр-инженер по эксплуатации ЛКС",
    "seller": "Продавец (Розничная сеть МТС)",
}


async def generate_scenario_for_skill(skill: str, role_name: str, skill_count: int) -> dict:
    """Генерирует ОДИН качественный сценарий для конкретного навыка"""

    prompt = f"""
Ты — эксперт по оценке кандидатов в МТС. Придумай РЕАЛИСТИЧНУЮ рабочую ситуацию для проверки навыка.

Роль: {role_name}
Навык для проверки: "{skill}"

Требования:
1. Ситуация должна быть РЕАЛЬНОЙ из рабочей практики (не абстрактной)
2. Вопрос должен проверять именно этот навык
3. 4 варианта ответа + "Свой вариант":
   - Один явно слабый (пассивность, незнание)
   - Один средний (базовое понимание)
   - Один хороший (проактивность, опыт)
   - Один отличный (стратегическое мышление)
   - "Свой вариант"

Верни СТРОГО JSON:
{{
    "id": "{role_name.lower().replace(' ', '_')}_hh_{skill_count}",
    "text": "Текст ситуации с вопросом (2-3 предложения)",
    "options": ["Вариант A", "Вариант B", "Вариант C", "Вариант D", "Свой вариант"],
    "skill_tested": "{skill}"
}}

Никакого текста кроме JSON. Ситуация должна быть КОНКРЕТНОЙ и РЕАЛЬНОЙ.
"""
    try:
        content = await _call_openai_with_fallback(
            messages=[
                {"role": "system", "content": "Ты — HR-эксперт по оценке кандидатов. Отвечай строго JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=600
        )
        content = content.strip().strip("```json").strip("```").strip()
        return json.loads(content)
    except Exception as e:
        print(f"  ⚠️ AI ошибка для {skill}: {e}")
        return None


async def generate_hh_scenarios():
    """Генерирует сценарии для всех ролей из hh_requirements.json"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.join(current_dir, '..', 'data', 'hh_requirements.json')

    if not os.path.exists(req_path):
        print(f"❌ Файл {req_path} не найден")
        return

    with open(req_path, 'r', encoding='utf-8') as f:
        requirements_data = json.load(f)

    all_scenarios = []

    for hh_role_id, role_data in requirements_data.items():
        if "error" in role_data:
            continue

        mts_role_id = ROLE_MAPPING.get(hh_role_id, hh_role_id)
        role_name = ROLE_NAMES.get(mts_role_id, role_data.get("role_name", hh_role_id))

        # Берём TOP skills (они релевантнее чем requirements)
        skills = role_data.get("skills", [])
        if not skills:
            print(f"⏭️ {role_name}: нет навыков, пропускаю")
            continue

        # Сортируем по count и берём топ-4
        sorted_skills = sorted(skills, key=lambda x: x.get("count", 0), reverse=True)
        top_skills = sorted_skills[:4]

        print(f"\n🎯 {role_name} — генерирую сценарии для навыков: {[s['skill'] for s in top_skills]}")

        role_questions = []
        for i, skill_data in enumerate(top_skills):
            skill_name = skill_data.get("skill", "")
            if not skill_name:
                continue

            scenario = await generate_scenario_for_skill(skill_name, role_name, i + 1)
            if scenario and scenario.get("text"):
                role_questions.append(scenario)
                print(f"  ✅ {skill_name}: {scenario['text'][:60]}...")

        if role_questions:
            all_scenarios.append({
                "role_id": mts_role_id,
                "role_name": role_name,
                "source": "hh.ru",
                "questions": role_questions
            })

    # Сохраняем
    data_dir = os.path.join(current_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, 'scenarios_from_hh.json')

    output = {
        "total_roles": len(all_scenarios),
        "generated_by": "AI from HH.ru skills",
        "scenarios": all_scenarios
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Сгенерировано {len(all_scenarios)} ролей, сохранено в {out_path}")
    return output


if __name__ == "__main__":
    asyncio.run(generate_hh_scenarios())

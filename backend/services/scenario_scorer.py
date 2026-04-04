"""
Rule-based скоринг сценариев — мгновенно, без AI.

Каждый ответ имеет вес (score 0-20).
Итоговый % = (сумма баллов / макс. возможных) × 100
"""

import logging

logger = logging.getLogger(__name__)


def score_scenario(questions: list, answers: list) -> dict:
    """
    Скоринг ответов на сценарий.

    Args:
        questions: [{"id": str, "options": [{"text": str, "score": int}], "type": "test"|"situation"}]
        answers: [{"question_id": str, "answer": str, "type": "test"|"situation"}]

    Returns:
        {
            "match_score": int (0-100),
            "total_score": int,
            "max_score": int,
            "answered": int,
            "details": [{"question_id": str, "score": int, "max": int}]
        }
    """
    total_score = 0
    max_score = 0
    answered = 0
    details = []

    for q in questions:
        q_id = q.get("id", "")
        options = q.get("options", [])
        q_type = q.get("type", "test")
        max_q_score = max((o.get("score", 0) for o in options), default=20)
        max_score += max_q_score

        # Находим ответ пользователя
        user_answer = None
        answer_type = "test"
        for a in answers:
            if a.get("question_id") == q_id:
                user_answer = a.get("answer", "")
                answer_type = a.get("type", "test")
                break

        if user_answer:
            answered += 1
            q_score = 0

            if q_type == "situation" or answer_type == "situation":
                # СИТУАЦИЯ: оцениваем по длине и наличию ключевых слов
                # Чем подробнее ответ — тем выше балл
                answer_words = len(user_answer.split())

                if answer_words >= 20:
                    # Развёрнутый ответ — 70-90% от максимума
                    q_score = round(max_q_score * 0.8)
                elif answer_words >= 10:
                    # Средний ответ — 50-70%
                    q_score = round(max_q_score * 0.6)
                elif answer_words >= 3:
                    # Короткий — 30-50%
                    q_score = round(max_q_score * 0.4)
                else:
                    # Слишком короткий — минимум
                    q_score = round(max_q_score * 0.2)

            else:
                # ТЕСТ: ищем совпадение ответа с вариантом
                for opt in options:
                    opt_text = opt.get("text", "").lower()
                    if opt_text == user_answer.lower() or opt_text in user_answer.lower() or user_answer.lower() in opt_text:
                        q_score = opt.get("score", 0)
                        break

                # Если точного совпадения нет — берём средний балл (10)
                if q_score == 0 and user_answer != "Свой вариант":
                    q_score = 10

            total_score += q_score
            details.append({"question_id": q_id, "score": q_score, "max": max_q_score, "type": q_type})

    # Процент
    match_score = round((total_score / max_score) * 100) if max_score > 0 else 0
    match_score = min(match_score, 100)

    # Уровень
    if match_score >= 80:
        level_label = "Отличный результат"
    elif match_score >= 60:
        level_label = "Хороший результат"
    elif match_score >= 40:
        level_label = "Средний результат"
    else:
        level_label = "Нужно подтянуть знания"

    return {
        "match_score": match_score,
        "total_score": total_score,
        "max_score": max_score,
        "answered": answered,
        "total_questions": len(questions),
        "level_label": level_label,
        "details": details,
    }


def score_scenario_with_feedback(questions: list, answers: list) -> dict:
    """Скоринг + фидбек по каждому вопросу"""
    result = score_scenario(questions, answers)

    # Добавляем фидбек
    feedback = []
    for detail in result["details"]:
        q_score = detail["score"]
        q_max = detail["max"]
        ratio = q_score / q_max if q_max > 0 else 0

        if ratio >= 0.9:
            fb = "Отлично! Глубокое понимание."
        elif ratio >= 0.7:
            fb = "Хорошо, но есть куда расти."
        elif ratio >= 0.5:
            fb = "Средне, стоит подучить тему."
        else:
            fb = "Слабо, нужно больше подготовки."

        feedback.append({
            "question_id": detail["question_id"],
            "score": q_score,
            "max": q_max,
            "feedback": fb,
        })

    result["feedback"] = feedback
    return result

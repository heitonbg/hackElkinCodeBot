import { useState } from 'react'
import { api } from '../api/client'

const QUICK_QUESTIONS = [
  { id: 'education', text: '🎓 Какое у тебя образование?', options: ['Школа', 'Колледж', 'Бакалавр', 'Магистр', 'Другое'] },
  { id: 'experience', text: '💼 Какой у тебя опыт?', options: ['Нет опыта', 'Стажировка', '1-2 года', '3-5 лет', '5+ лет'] },
  { id: 'field', text: '🎯 Какое направление интересно?', options: ['IT / Программирование', 'Аналитика / Данные', 'Продажи', 'Маркетинг', 'HR', 'Юриспруденция', 'Инженерия', 'Дизайн'] },
  { 
    id: 'skills', 
    text: '🛠️ Какие навыки уже есть? (выбери 3-5)', 
    options: [
      'Python', 'SQL', 'JavaScript', 'Java', 'Git', 'Docker', 'Linux',
      'Excel', '1С', 'Английский язык', 'Коммуникация', 'Переговоры', 
      'Продажи', 'Аналитика данных', 'Управление проектами', 'Рекрутинг'
    ], 
    multi: true 
  },
  { id: 'goal', text: '🚀 Какая цель?', options: ['Найти первую работу', 'Сменить профессию', 'Повышение', 'Стажировка', 'Прокачать навыки'] }
]

export default function QuickOnboarding({ onComplete }) {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState({})
  const [multiSelect, setMultiSelect] = useState([])
  const [loading, setLoading] = useState(false)

  const current = QUICK_QUESTIONS[step]
  const isLast = step === QUICK_QUESTIONS.length - 1

  const handleNext = async () => {
    // Сохраняем ответ
    if (current.multi) {
      setAnswers({ ...answers, [current.id]: multiSelect })
    } else {
      setAnswers({ ...answers, [current.id]: multiSelect[0] || '' })
    }

    if (isLast) {
      setLoading(true)
      
      // Сохраняем онбординг в БД
      await api.saveOnboarding({
        telegram_id: 'demo_user',
        education: answers.education || '',
        experience: answers.experience || '',
        field: answers.field || '',
        skills: answers.skills || [],
        career_goals: [answers.goal || ''],
        interests: []
      })
      
      // Получаем AI-рекомендации
      let analysis = null
      try {
        const result = null // await api.quickMatch2()
        analysis = result
        console.log('📦 AI вернул:', analysis)
      } catch (err) {
        console.error('AI ошибка:', err)
      }
      
      // Если AI не вернул профессии — используем мок
      let professionsToUse = analysis?.professions
      if (!professionsToUse || professionsToUse.length === 0) {
        console.log('⚠️ Использую мок-профессии')
        professionsToUse = [
          { title: "Стажёр продаж", match_percent: 85, reason: "Отличная коммуникация и работа с людьми" },
          { title: "Стажёр HR", match_percent: 78, reason: "Интерес к рекрутингу и работе с кандидатами" },
          { title: "Маркетолог", match_percent: 72, reason: "Креативное мышление и аналитика" },
          { title: "Аналитик данных", match_percent: 68, reason: "Навыки Excel и аналитический склад ума" },
          { title: "IT-стажёр", match_percent: 65, reason: "Технические навыки и интерес к IT" },
          { title: "Специалист закупок", match_percent: 55, reason: "Внимательность к деталям и документам" }
        ]
      }
      
      setLoading(false)
      onComplete(answers, { professions: professionsToUse })
    } else {
      setStep(step + 1)
      setMultiSelect([])
    }
  }

  const toggleMulti = (opt) => {
    setMultiSelect(prev => 
      prev.includes(opt) ? prev.filter(o => o !== opt) : [...prev, opt]
    )
  }

  const progress = ((step + 1) / QUICK_QUESTIONS.length) * 100

  return (
    <div className="onboarding-container">
      <div style={{ padding: 24 }}>
        {/* Прогресс */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, color: 'white', fontSize: '0.85rem' }}>
            <span>Шаг {step + 1} из {QUICK_QUESTIONS.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.2)' }}>
            <div className="progress-fill" style={{ width: `${progress}%`, background: 'white' }} />
          </div>
        </div>
        
        {/* Вопрос */}
        <h2 style={{ marginBottom: 24, textAlign: 'center', color: 'white' }}>{current.text}</h2>
        
        {/* Варианты ответов */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center', marginBottom: 32 }}>
          {current.options.map(opt => (
            <button
              key={opt}
              onClick={() => current.multi ? toggleMulti(opt) : setMultiSelect([opt])}
              className={`onboarding-option ${multiSelect.includes(opt) ? 'selected' : ''}`}
              style={{
                padding: '10px 20px',
                borderRadius: 30,
                background: multiSelect.includes(opt) ? 'white' : 'rgba(255,255,255,0.2)',
                color: multiSelect.includes(opt) ? 'var(--primary)' : 'white',
                border: 'none',
                cursor: 'pointer',
                fontSize: '0.95rem',
                transition: 'all 0.2s'
              }}
            >
              {opt}
            </button>
          ))}
        </div>
        
        {/* Кнопка далее */}
        <button 
          className="btn btn-primary" 
          onClick={handleNext}
          disabled={multiSelect.length === 0 || loading}
          style={{
            width: '100%',
            padding: '14px',
            fontSize: '1rem',
            background: multiSelect.length > 0 ? 'white' : 'rgba(255,255,255,0.3)',
            color: multiSelect.length > 0 ? 'var(--primary)' : 'white',
            border: 'none',
            borderRadius: 12,
            cursor: multiSelect.length > 0 ? 'pointer' : 'not-allowed'
          }}
        >
          {loading ? '⏳ Анализируем...' : (isLast ? '🎯 Подобрать профессии →' : 'Далее →')}
        </button>
      </div>
    </div>
  )
}
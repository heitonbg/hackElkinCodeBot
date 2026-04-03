import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

// Шаги анкеты — универсальные, покрывающие все направления МТС
const STEPS = [
  {
    id: 'education',
    question: 'Какое у тебя образование?',
    subtitle: 'Это поможет подобрать подходящие направления',
    type: 'select',
    options: [
      'Школа (учусь / окончил)',
      'Колледж / техникум',
      'Бакалавриат',
      'Магистратура',
      'PhD / Аспирантура',
      'Другое',
    ],
  },
  {
    id: 'field',
    question: 'Какое у тебя направление?',
    subtitle: 'Выбери наиболее подходящее',
    type: 'select',
    options: [
      'IT и программирование',
      'Аналитика и данные',
      'Продажи и маркетинг',
      'HR и рекрутинг',
      'Юриспруденция и право',
      'Финансы и экономика',
      'Инженерия и телеком',
      'Дизайн и креатив',
      'Администрирование',
      'Другое',
    ],
  },
  {
    id: 'experience',
    question: 'Какой у тебя опыт работы?',
    subtitle: 'Честно — это влияет на подбор позиций',
    type: 'select',
    options: [
      'Нет опыта (ищу первую работу / стажировку)',
      'Стажировка / практика',
      '1-2 года',
      '3-5 лет',
      '5+ лет',
    ],
  },
  {
    id: 'interests',
    question: 'Что тебя привлекает?',
    subtitle: 'Можно выбрать несколько',
    type: 'multi',
    options: [
      '🖥️ Разработка ПО',
      '🤖 Искусственный интеллект / ML',
      '📊 Аналитика данных',
      '📱 Мобильная разработка',
      '🌐 Веб-разработка',
      '🔒 Кибербезопасность',
      '☁️ Облачные технологии / DevOps',
      '📈 Продажи и переговоры',
      '📢 Маркетинг и реклама',
      '👥 HR и подбор персонала',
      '⚖️ Юриспруденция',
      '💰 Финансы и аналитика',
      '🏗️ Инженерия и телеком',
      '🎨 Дизайн и UX',
      '📋 Управление проектами',
    ],
  },
  {
    id: 'skills',
    question: 'Какими навыками владеешь?',
    subtitle: 'Выбери всё, что применимо',
    type: 'multi',
    options: [
      'Python',
      'SQL',
      'JavaScript / TypeScript',
      'Java',
      'C# / .NET',
      'React / Vue / Angular',
      'Git',
      'Docker / Kubernetes',
      'Linux',
      'Excel / Google Sheets',
      'Power BI / Tableau',
      'Figma',
      'Английский язык',
      'Презентации и публичные выступления',
      'Работа с клиентами',
      'Управление командой',
      'Деловая переписка',
      'Анализ данных',
    ],
  },
  {
    id: 'career_goals',
    question: 'Какая у тебя цель?',
    subtitle: 'Это определит стратегию развития',
    type: 'multi',
    options: [
      '🚀 Найти первую работу в IT',
      '🔄 Сменить профессию',
      '📈 Получить повышение',
      '💻 Начать фриланс',
      '🎓 Пройти стажировку',
      '🏢 Войти в крупную компанию',
      '💡 Развить технические навыки',
      '🤝 Улучшить soft skills',
    ],
  },
]

export default function Onboarding() {
  const [step, setStep] = useState(0)
  const [data, setData] = useState({
    education: '',
    field: '',
    experience: '',
    interests: [],
    skills: [],
    career_goals: [],
  })
  const [multiSelect, setMultiSelect] = useState([])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const currentStep = STEPS[step]
  const isLastStep = step === STEPS.length - 1
  const canProceed = currentStep.type === 'select'
    ? multiSelect.length === 1
    : multiSelect.length >= 1

  const handleNext = () => {
    if (!canProceed) return

    if (currentStep.type === 'select') {
      setData({ ...data, [currentStep.id]: multiSelect[0] || '' })
    } else {
      setData({ ...data, [currentStep.id]: multiSelect })
    }

    if (isLastStep) {
      handleSubmit()
    } else {
      setStep(step + 1)
      setMultiSelect([])
    }
  }

  const handleBack = () => {
    if (step > 0) {
      setStep(step - 1)
      setMultiSelect([])
    }
  }

  const toggleOption = (option) => {
    if (currentStep.type === 'multi') {
      setMultiSelect(prev =>
        prev.includes(option) ? prev.filter(o => o !== option) : [...prev, option]
      )
    } else {
      setMultiSelect([option])
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      await api.saveOnboarding(data)
      navigate('/dashboard')
    } catch (err) {
      console.error('Onboarding error:', err)
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="onboarding-container">
      <div className="onboarding-step">
        {/* Прогресс */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.85rem', opacity: 0.9 }}>
            <span>Шаг {step + 1} из {STEPS.length}</span>
            <span>{Math.round(((step + 1) / STEPS.length) * 100)}%</span>
          </div>
          <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.2)' }}>
            <div
              className="progress-fill"
              style={{ width: `${((step + 1) / STEPS.length) * 100}%`, background: 'white' }}
            />
          </div>
        </div>

        {/* Вопрос */}
        <h2 className="onboarding-question">{currentStep.question}</h2>
        {currentStep.subtitle && (
          <p style={{ textAlign: 'center', opacity: 0.9, marginBottom: 24, fontSize: '0.95rem' }}>
            {currentStep.subtitle}
          </p>
        )}

        {/* Опции */}
        <div className="onboarding-options">
          {currentStep.options.map(option => (
            <button
              key={option}
              className={`onboarding-option ${multiSelect.includes(option) ? 'selected' : ''}`}
              onClick={() => toggleOption(option)}
            >
              {option}
            </button>
          ))}
        </div>

        {/* Навигация */}
        <div className="onboarding-nav">
          {step > 0 && (
            <button
              className="btn btn-secondary"
              onClick={handleBack}
              style={{ background: 'rgba(255,255,255,0.2)', color: 'white' }}
            >
              ← Назад
            </button>
          )}
          <button
            className="btn btn-primary"
            onClick={handleNext}
            style={{ background: multiSelect.length > 0 ? 'white' : 'rgba(255,255,255,0.4)', color: 'var(--mts-red)' }}
            disabled={!canProceed || loading}
          >
            {loading ? '⏳ Сохраняю...' : isLastStep ? '🚀 Начать' : 'Далее →'}
          </button>
        </div>

        {/* Демо кнопка */}
        <div style={{ marginTop: 24, textAlign: 'center' }}>
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              background: 'rgba(255,255,255,0.15)',
              border: '1px solid rgba(255,255,255,0.3)',
              color: 'white',
              padding: '8px 16px',
              borderRadius: 12,
              cursor: 'pointer',
              fontSize: '0.85rem',
            }}
          >
            ⚡ Пропустить и посмотреть демо
          </button>
        </div>
      </div>
    </div>
  )
}

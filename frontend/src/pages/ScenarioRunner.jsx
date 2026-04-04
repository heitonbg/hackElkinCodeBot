import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { api } from '../api/client'

export default function ScenarioRunner() {
  const navigate = useNavigate()
  const location = useLocation()
  
  // Получаем роли из state или из localStorage (fallback)
  const [roles, setRoles] = useState(() => {
    const stateRoles = location.state?.roles || []
    if (stateRoles.length === 0) {
      // Пробуем загрузить из localStorage
      try {
        const stored = localStorage.getItem('pending_scenario_roles')
        if (stored) {
          const parsed = JSON.parse(stored)
          console.log('📦 Loaded roles from localStorage:', parsed)
          return parsed
        }
      } catch (e) {
        console.error('Failed to load roles from localStorage:', e)
      }
    }
    return stateRoles
  })

  const [scenarios, setScenarios] = useState([])
  const [currentRoleIndex, setCurrentRoleIndex] = useState(0)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [customAnswer, setCustomAnswer] = useState('')
  const [results, setResults] = useState({})

  useEffect(() => {
    console.log(' ScenarioRunner mounted, roles:', roles)
    if (roles.length === 0) {
      console.warn('⚠️ No roles, redirecting to diagnostic')
      navigate('/diagnostic')
      return
    }
    loadScenarios()
  }, [roles])

  async function loadScenarios() {
    setLoading(true)
    try {
      console.log('📦 Loading scenarios for roles:', roles.map(r => r.role_id))
      const loaded = []
      for (const roleData of roles) {
        // Быстрая загрузка сценария из БД
        const scenario = await api.getScenario(roleData.role_id, 'junior')
        console.log(`📋 Scenario for ${roleData.role_id}:`, scenario)
        if (scenario && !scenario.error) {
          loaded.push({
            role_id: scenario.role_id,
            role_name: scenario.title || roleData.title,
            questions: scenario.questions || [],
          })
        } else {
          console.warn(`⚠️ No scenario for ${roleData.role_id}`)
        }
      }

      if (loaded.length === 0) {
        console.error('❌ No scenarios loaded, redirecting to diagnostic')
        navigate('/diagnostic')
        return
      }

      console.log('✅ Loaded scenarios:', loaded.map(s => ({ role_id: s.role_id, questions: s.questions.length })))
      // Очищаем localStorage после успешной загрузки
      localStorage.removeItem('pending_scenario_roles')

      setScenarios(loaded)

      const initAnswers = {}
      for (const s of loaded) initAnswers[s.role_id] = []
      setAnswers(initAnswers)
      setLoading(false)
    } catch (err) {
      console.error('Load scenarios error:', err)
      setLoading(false)
    }
  }

  const currentScenario = scenarios[currentRoleIndex]
  const currentQuestion = currentScenario?.questions?.[currentQuestionIndex]
  const isLastQuestion = currentQuestionIndex >= (currentScenario?.questions?.length || 1) - 1
  const isLastRole = currentRoleIndex >= scenarios.length - 1

  const handleAnswer = (option) => {
    if (!currentScenario) return
    const roleId = currentScenario.role_id
    const answerText = option === 'Свой вариант' ? customAnswer : option

    setAnswers(prev => {
      const roleAnswers = prev[roleId] || []
      const existingIndex = roleAnswers.findIndex(a => a.question_id === currentQuestion.id)
      if (existingIndex >= 0) {
        const updated = [...roleAnswers]
        updated[existingIndex] = { question_id: currentQuestion.id, answer: answerText }
        return { ...prev, [roleId]: updated }
      }
      return { ...prev, [roleId]: [...roleAnswers, { question_id: currentQuestion.id, answer: answerText }] }
    })

    setCustomAnswer('')

    if (isLastQuestion) {
      if (isLastRole) {
        submitAll()
      } else {
        setCurrentRoleIndex(currentRoleIndex + 1)
        setCurrentQuestionIndex(0)
      }
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  async function submitAll() {
    setSubmitting(true)
    try {
      const allResults = []

      // Мгновенный rule-based скоринг для каждой роли
      for (const scenario of scenarios) {
        const roleAnswers = answers[scenario.role_id] || []
        if (roleAnswers.length > 0) {
          const result = await api.scoreScenario(scenario.role_id, 'junior', roleAnswers)
          allResults.push(result)
        }
      }

      setResults(allResults)

      // Переход на дашборд — результаты мгновенны, AI в фоне
      try { await api.completeRetest() } catch (e) {}
      navigate('/dashboard')
    } catch (err) {
      console.error('Submit error:', err)
      navigate('/dashboard')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="loading"><div className="spinner" /></div>
  }

  if (scenarios.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ fontSize: '4rem', marginBottom: 16 }}>😕</div>
        <h2>Нет ситуаций для выбранных ролей</h2>
        <button className="btn btn-primary" onClick={() => navigate('/diagnostic')}>← Пройти диагностику</button>
      </div>
    )
  }

  const totalQuestions = scenarios.reduce((acc, s) => acc + (s.questions?.length || 0), 0)
  const currentTotal = scenarios.slice(0, currentRoleIndex).reduce((acc, s) => acc + (s.questions?.length || 0), 0) + currentQuestionIndex
  const progress = (currentTotal / totalQuestions) * 100

  return (
    <div className="onboarding-container">
      <div className="onboarding-step">
        {/* Прогресс */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: '0.85rem', opacity: 0.8 }}>
            <span>{currentScenario.role_name}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.15)' }}>
            <div className="progress-fill" style={{ width: `${progress}%`, background: 'var(--primary)' }} />
          </div>
        </div>

        {/* Индикатор */}
        <div style={{ textAlign: 'center', marginBottom: 12 }}>
          <span style={{
            padding: '4px 12px', borderRadius: 16,
            background: 'rgba(255,255,255,0.1)', fontSize: '0.8rem',
          }}>
            Роль {currentRoleIndex + 1}/{scenarios.length} • Вопрос {currentQuestionIndex + 1}/{currentScenario.questions.length}
          </span>
        </div>

        {/* Вопрос */}
        <h2 className="onboarding-question" style={{ fontSize: '1.1rem', marginBottom: 20 }}>
          {currentQuestion?.text}
        </h2>

        {/* Варианты */}
        <div className="onboarding-options">
          {(currentQuestion?.options || []).map((option, i) => {
            const optionText = typeof option === 'string' ? option : option.text
            return (
              <button key={i} className="onboarding-option" onClick={() => handleAnswer(optionText)}
                style={{ textAlign: 'left', fontSize: '0.9rem', padding: '12px 16px' }}>
                {optionText}
              </button>
            )
          })}
        </div>

        {/* Свой вариант */}
        {currentQuestion?.options?.some(o => (typeof o === 'string' ? o : o.text) === 'Свой вариант') && (
          <div style={{ marginTop: 12 }}>
            <input type="text" className="onboarding-input" placeholder="Твой вариант..."
              value={customAnswer} onChange={(e) => setCustomAnswer(e.target.value)}
              style={{ width: '100%', padding: '12px 16px', borderRadius: 12, border: '2px solid rgba(255,255,255,0.3)', background: 'rgba(255,255,255,0.1)', color: 'white', fontSize: '0.95rem', outline: 'none' }}
            />
            <button onClick={() => customAnswer.trim() && handleAnswer('Свой вариант')} disabled={!customAnswer.trim()}
              style={{ marginTop: 8, padding: '10px 20px', borderRadius: 12, background: customAnswer.trim() ? 'white' : 'rgba(255,255,255,0.3)', color: 'var(--primary)', border: 'none', cursor: customAnswer.trim() ? 'pointer' : 'not-allowed', fontWeight: 600, width: '100%' }}>
              Отправить
            </button>
          </div>
        )}

        {submitting && <div className="loading"><div className="spinner" /></div>}
      </div>
    </div>
  )
}

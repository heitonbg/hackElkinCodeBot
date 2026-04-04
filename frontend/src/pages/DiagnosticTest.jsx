import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function DiagnosticTest() {
  const navigate = useNavigate()
  const [questions, setQuestions] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [results, setResults] = useState(null)

  useEffect(() => {
    loadQuestions()
  }, [])

  async function loadQuestions() {
    try {
      const data = await api.getDiagnosticQuestions()
      setQuestions(data.questions || [])
    } catch (err) {
      console.error('Load questions error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAnswer = (answerText) => {
    const newAnswers = [...answers]
    newAnswers[currentQuestion] = {
      question_id: questions[currentQuestion].id,
      answer: answerText,
    }
    setAnswers(newAnswers)

    // Переход к следующему вопросу или завершение
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      submitDiagnostic(newAnswers)
    }
  }

  async function submitDiagnostic(finalAnswers) {
    setSubmitting(true)
    try {
      const result = await api.runDiagnostic(finalAnswers)
      setResults(result)
      // Сохраняем результаты для CareerPath
      localStorage.setItem('diagnostic_results', JSON.stringify(result))
    } catch (err) {
      console.error('Diagnostic error:', err)
      // В случае ошибки — переходим на career
      navigate('/career')
    } finally {
      setSubmitting(false)
    }
  }

  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100

  // Экран результатов
  if (results) {
    return (
      <div className="onboarding-container">
        <div className="onboarding-step">
          <div style={{ textAlign: 'center', marginBottom: 24 }}>
            <div style={{ fontSize: '4rem', marginBottom: 12 }}>🎯</div>
            <h2 style={{ marginBottom: 8 }}>Твои подходящие роли</h2>
            <p className="text-muted">На основе твоих ответов мы подобрали профессии</p>
          </div>

          {/* Топ категории */}
          {results.top_categories && results.top_categories.length > 0 && (
            <div className="card" style={{ marginBottom: 16 }}>
              <h3 style={{ marginBottom: 12 }}>📊 Твои сильные стороны</h3>
              {results.top_categories.slice(0, 3).map((cat, i) => {
                const emojiMap = {
                  'it_and_development': '💻', 'data_and_analytics': '📊', 'design_and_creative': '🎨',
                  'marketing_and_sales': '📢', 'management': '👔', 'finance_and_accounting': '💰',
                  'healthcare': '🏥', 'education': '📚', 'engineering_and_manufacturing': '⚙️',
                  'media_and_entertainment': '🎬', 'hr_and_recruitment': '🤝', 'legal': '⚖️',
                  'customer_service': '🎧', 'science_and_research': '🔬', 'retail': '🛒',
                }
                const emoji = emojiMap[cat.category_id] || '💼'
                return (
                  <div key={cat.category_id} style={{ marginBottom: i < 2 ? 12 : 0 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, alignItems: 'center' }}>
                      <span style={{ fontSize: '0.9rem' }}>{emoji} {cat.category_name}</span>
                      <span style={{ fontWeight: 700, color: 'var(--primary)' }}>{cat.score}%</span>
                    </div>
                    <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.1)', height: '8px', borderRadius: '4px' }}>
                      <div className="progress-fill" style={{ width: `${cat.score}%`, background: 'var(--primary)', height: '100%', borderRadius: '4px' }} />
                    </div>
                  </div>
                )
              })}
            </div>
          )}

          {/* Рекомендованные роли */}
          <div className="card">
            <h3 style={{ marginBottom: 12 }}>💼 Рекомендуем попробовать</h3>
            <p className="text-muted text-sm" style={{ marginBottom: 12 }}>
              Выбери одну или несколько — по каждой будет тест
            </p>

            {results.recommended_roles?.slice(0, 8).map((role) => (
              <button
                key={role.role_id}
                onClick={() => {
                  console.log('🎯 Navigating to scenario-runner with role:', role)
                  // Сохраняем роль в localStorage как fallback
                  localStorage.setItem('pending_scenario_roles', JSON.stringify([role]))
                  navigate('/scenario-runner', { state: { roles: [role] } })
                }}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '12px 14px', borderRadius: 12, marginBottom: 8,
                  border: '2px solid rgba(255,255,255,0.12)',
                  background: 'rgba(255,255,255,0.04)',
                  cursor: 'pointer', width: '100%', textAlign: 'left',
                  transition: 'all 0.2s',
                }}
                onMouseEnter={(e) => e.target.style.background = 'rgba(255,255,255,0.08)'}
                onMouseLeave={(e) => e.target.style.background = 'rgba(255,255,255,0.04)'}
              >
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: '1.5rem' }}>{role.category_emoji || '💼'}</span>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{role.title}</div>
                    <div className="text-muted text-sm">{role.category_emoji || ''} {role.category}</div>
                  </div>
                </div>
                <span style={{
                  padding: '4px 10px', borderRadius: 12, fontSize: '0.8rem', fontWeight: 700,
                  background: role.match_percent >= 70 ? 'rgba(0,184,148,0.15)' : role.match_percent >= 50 ? 'rgba(253,203,110,0.15)' : 'rgba(225,112,85,0.15)',
                  color: role.match_percent >= 70 ? 'var(--success)' : role.match_percent >= 50 ? '#e17055' : 'var(--danger)',
                }}>
                  {role.match_percent}%
                </span>
              </button>
            ))}
          </div>

          {/* Кнопка продолжить */}
          <button
            className="btn btn-primary"
            style={{ width: '100%', marginTop: 16 }}
            onClick={() => navigate('/career')}
          >
            Продолжить →
          </button>
        </div>
      </div>
    )
  }

  if (loading) {
    return <div className="loading"><div className="spinner" /></div>
  }

  if (questions.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: 40 }}>
        <div style={{ fontSize: '4rem', marginBottom: 16 }}>😕</div>
        <h2>Не удалось загрузить вопросы</h2>
        <button className="btn btn-primary" onClick={() => navigate('/career')}>← На главную</button>
      </div>
    )
  }

  const q = questions[currentQuestion]

  return (
    <div className="onboarding-container">
      <div className="onboarding-step">
        {/* Прогресс */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.85rem', opacity: 0.9 }}>
            <span>Вопрос {currentQuestion + 1} из {questions.length}</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.2)' }}>
            <div
              className="progress-fill"
              style={{ width: `${progress}%`, background: 'white' }}
            />
          </div>
        </div>

        {/* Вопрос */}
        <h2 className="onboarding-question">{q.text}</h2>

        {/* Варианты */}
        <div className="onboarding-options">
          {q.options.map((option, i) => (
            <button
              key={i}
              className="onboarding-option"
              onClick={() => handleAnswer(option.text)}
              style={{ textAlign: 'left', fontSize: '0.95rem', padding: '14px 18px' }}
            >
              {option.text}
            </button>
          ))}
        </div>

        {/* Навигация */}
        <div className="onboarding-nav">
          {currentQuestion > 0 && (
            <button
              className="btn btn-secondary"
              onClick={handleBack}
              style={{ background: 'rgba(255,255,255,0.2)', color: 'white' }}
            >
              ← Назад
            </button>
          )}
        </div>

        {submitting && (
          <div className="loading" style={{ marginTop: 20 }}>
            <div className="spinner" />
            <p style={{ marginTop: 12, opacity: 0.8 }}>Анализируем твои ответы...</p>
          </div>
        )}
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function ScenarioTest({ recommendedRoles = [], userData = {}, onComplete }) {
  console.log('🎯 ScenarioTest получил recommendedRoles:', recommendedRoles)
  const [scenarios, setScenarios] = useState([])
  const [selectedRoles, setSelectedRoles] = useState([])
  const [showRoleSelector, setShowRoleSelector] = useState(true)
  const [currentRoleIndex, setCurrentRoleIndex] = useState(0)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)
  const [customInputVisible, setCustomInputVisible] = useState({})
  const [customInputValue, setCustomInputValue] = useState({})
  const navigate = useNavigate()

  // Загружаем сценарии только для выбранных ролей
  useEffect(() => {
    loadScenarios()
  }, [])

  async function loadScenarios() {
    try {
      // Временно используем оба источника
      let data
      try {
        data = await api.getHhScenarios()
        if (data.error) throw new Error(data.error)
      } catch (e) {
        console.log('HH сценарии не найдены, использую статические')
        data = await api.getScenarios()
      }
      
      const allScenarios = data.scenarios || []
      setScenarios(allScenarios)
    } catch (err) {
      console.error('Load scenarios error:', err)
    } finally {
      setLoading(false)
    }
  }

  const currentRole = scenarios[currentRoleIndex]
  const currentQuestion = currentRole?.questions?.[currentQuestionIndex]
  
  const getCurrentAnswer = () => {
    const key = `${currentRole?.role_id}_${currentQuestion?.id}`
    return answers[key] || ''
  }

  const handleSelectOption = (option) => {
    const key = `${currentRole.role_id}_${currentQuestion.id}`
    
    if (option === 'Свой вариант' || option.toLowerCase().includes('свой')) {
      setCustomInputVisible({ ...customInputVisible, [key]: true })
      setAnswers({ ...answers, [key]: '' })
    } else {
      setCustomInputVisible({ ...customInputVisible, [key]: false })
      setAnswers({ ...answers, [key]: option })
    }
  }

  const handleCustomInputChange = (value) => {
    const key = `${currentRole.role_id}_${currentQuestion.id}`
    setCustomInputValue({ ...customInputValue, [key]: value })
    setAnswers({ ...answers, [key]: value })
  }

  const isAnswerSelected = () => {
    const answer = getCurrentAnswer()
    return answer && answer.trim().length > 0
  }

  const handleNext = () => {
    if (!isAnswerSelected()) return

    if (currentQuestionIndex < currentRole.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else if (currentRoleIndex < scenarios.length - 1) {
      setCurrentRoleIndex(currentRoleIndex + 1)
      setCurrentQuestionIndex(0)
    } else {
      handleAnalyze()
    }
  }

  const handleBack = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    } else if (currentRoleIndex > 0) {
      setCurrentRoleIndex(currentRoleIndex - 1)
      setCurrentQuestionIndex(scenarios[currentRoleIndex - 1]?.questions.length - 1 || 0)
    }
  }

  async function handleAnalyze() {
    setAnalyzing(true)
    try {
      const results = []
      for (const role of scenarios) {
        const roleAnswers = []
        for (const q of role.questions) {
          const key = `${role.role_id}_${q.id}`
          if (answers[key]) {
            roleAnswers.push({
              question_id: q.id,
              question_text: q.text,
              answer: answers[key]
            })
          }
        }
        if (roleAnswers.length > 0) {
          const result = await api.analyzeScenario(role.role_id, roleAnswers)
          results.push({
            role_id: role.role_id,
            role_name: role.role_name,
            ...result
          })
        }
      }
      
      results.sort((a, b) => b.match_score - a.match_score)
      setResult(results)
      localStorage.setItem('scenario_results', JSON.stringify(results))
      
    } catch (err) {
      console.error('Analysis error:', err)
    } finally {
      setAnalyzing(false)
    }
  }

  const handleSelectRole = (role) => {
    localStorage.setItem('selected_role', JSON.stringify(role))
    navigate('/dashboard')
  }

  // Экран выбора ролей (через чекбоксы)
  // Экран выбора ролей (через чекбоксы)
    if (showRoleSelector && recommendedRoles.length > 0) {
    return (
        <div>
        <div className="page-header">
            <h1>🎯 Выбери направления</h1>
            <p>Отметь те, которые тебе интересны (2-3 штуки)</p>
        </div>
        <div style={{ padding: 16 }}>
            {recommendedRoles.map((role, idx) => (
            <div key={idx} className="vacancy-card" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <input
                type="checkbox"
                checked={selectedRoles.includes(role.title)}
                onChange={(e) => {
                    if (e.target.checked) {
                    setSelectedRoles([...selectedRoles, role.title])
                    } else {
                    setSelectedRoles(selectedRoles.filter(r => r !== role.title))
                    }
                }}
                style={{ width: 24, height: 24, accentColor: 'var(--primary)' }}
                />
                <div style={{ flex: 1 }}>
                <h3>{role.title}</h3>
                <div className={`vacancy-match ${
                    role.match_percent >= 70 ? 'vacancy-match-high' : 
                    role.match_percent >= 40 ? 'vacancy-match-medium' : 'vacancy-match-low'
                }`} style={{ display: 'inline-block' }}>
                    {role.match_percent}% совпадение
                </div>
                <p className="text-muted text-sm" style={{ marginTop: 4 }}>{role.reason?.slice(0, 100)}...</p>
                </div>
            </div>
            ))}
            
            {/* Кнопка "Выбрать всё" — оставляем */}
            <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
            <button 
                className="btn btn-secondary" 
                style={{ flex: 1 }}
                onClick={() => {
                const allTitles = recommendedRoles.map(r => r.title)
                setSelectedRoles(allTitles)
                }}
            >
                ✅ Выбрать всё
            </button>
            <button 
                className="btn btn-primary" 
                style={{ flex: 1 }}
                onClick={async () => {
                if (selectedRoles.length === 0) {
                    alert('Выбери хотя бы одно направление')
                    return
                }
                
                // Фильтруем сценарии по выбранным ролям
                const allScenarios = await api.getScenarios()
                const filtered = allScenarios.scenarios.filter(s =>
                    selectedRoles.some(roleTitle => 
                    s.role_name.toLowerCase().includes(roleTitle.toLowerCase()) ||
                    roleTitle.toLowerCase().includes(s.role_name.toLowerCase())
                    )
                )
                
                if (filtered.length === 0) {
                    alert('Не найдено сценариев для выбранных ролей')
                    return
                }
                
                setScenarios(filtered)
                setShowRoleSelector(false)
                setCurrentRoleIndex(0)
                setCurrentQuestionIndex(0)
                setAnswers({})
                }}
            >
                🚀 Пройти сценарии ({selectedRoles.length})
            </button>
            </div>
        </div>
        </div>
    )
    }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    )
  }

  if (result) {
    return (
      <div>
        <div className="page-header">
          <h1>🎯 Результаты диагностики</h1>
          <p>Вот какие роли тебе подходят</p>
        </div>
        <div style={{ padding: 16 }}>
          {result.map((role, i) => (
            <div
              key={role.role_id}
              className="vacancy-card"
              style={{ cursor: 'pointer' }}
              onClick={() => handleSelectRole(role)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h3>{role.role_name}</h3>
                <span className={`vacancy-match ${
                  role.match_score >= 70 ? 'vacancy-match-high' :
                  role.match_score >= 40 ? 'vacancy-match-medium' : 'vacancy-match-low'
                }`}>
                  {role.match_score}%
                </span>
              </div>
              <p className="text-muted text-sm" style={{ marginTop: 8 }}>{role.feedback}</p>
              {role.strengths?.length > 0 && role.strengths[0] !== '—' && (
                <div style={{ marginTop: 8 }}>
                  <span className="tag tag-primary">✅ {role.strengths[0]}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!currentRole || scenarios.length === 0) {
    return (
      <div style={{ padding: 16, textAlign: 'center' }}>
        <div className="card">
          <div style={{ fontSize: '3rem', marginBottom: 12 }}>🤔</div>
          <h3>Нет сценариев для выбранных ролей</h3>
          <p className="text-muted">Попробуй выбрать другие направления</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Назад к выбору
          </button>
        </div>
      </div>
    )
  }

  const totalQuestions = scenarios.reduce((acc, role) => acc + role.questions.length, 0)
  const answeredCount = Object.keys(answers).length
  const progress = (answeredCount / totalQuestions) * 100

  const currentAnswer = getCurrentAnswer()
  const key = `${currentRole.role_id}_${currentQuestion.id}`
  const showCustomInput = customInputVisible[key] || false

  return (
    <div>
      <div className="page-header">
        <h1>🧠 Карьерная диагностика</h1>
        <p>Ответь на вопросы — получи точные рекомендации</p>
      </div>

      <div style={{ padding: 16 }}>
        {/* Прогресс */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span className="text-muted text-sm">
              Вопрос {answeredCount} из {totalQuestions}
            </span>
            <span className="text-muted text-sm">{Math.round(progress)}%</span>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>

        {/* Карточка с вопросом */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="tag tag-primary" style={{ marginBottom: 12, display: 'inline-block' }}>
            {currentRole.role_name}
          </div>
          <h3 style={{ marginBottom: 20, lineHeight: 1.4 }}>{currentQuestion?.text}</h3>

          {/* Варианты ответов */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {currentQuestion?.options?.map((option, idx) => {
              const isCustomOption = option === 'Свой вариант'
              const isSelected = !isCustomOption && currentAnswer === option
              
              return (
                <button
                  key={idx}
                  className={`btn ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
                  onClick={() => handleSelectOption(option)}
                  style={{ 
                    textAlign: 'left', 
                    justifyContent: 'flex-start',
                    border: isCustomOption && showCustomInput ? '2px solid var(--primary)' : 'none'
                  }}
                >
                  {String.fromCharCode(65 + idx)}. {option}
                </button>
              )
            })}
          </div>

          {/* Поле для свободного ввода */}
          {showCustomInput && (
            <div style={{ marginTop: 16 }}>
              <label className="text-muted text-sm" style={{ display: 'block', marginBottom: 8 }}>
                ✍️ Напиши свой ответ:
              </label>
              <textarea
                className="chat-input"
                style={{
                  width: '100%',
                  minHeight: '100px',
                  padding: '12px',
                  borderRadius: '12px',
                  border: `2px solid var(--primary)`,
                  resize: 'vertical',
                  fontSize: '0.95rem',
                  lineHeight: 1.4,
                }}
                placeholder="Напиши свой вариант ответа здесь..."
                value={customInputValue[key] || ''}
                onChange={(e) => handleCustomInputChange(e.target.value)}
                autoFocus
              />
              <div className="text-muted text-sm" style={{ marginTop: 8, fontSize: '0.75rem' }}>
                💡 Чем подробнее ответ, тем точнее будет анализ
              </div>
            </div>
          )}
        </div>

        {/* Навигация */}
        <div style={{ display: 'flex', gap: 12 }}>
          <button
            className="btn btn-secondary"
            onClick={handleBack}
            disabled={currentRoleIndex === 0 && currentQuestionIndex === 0}
            style={{ flex: 1 }}
          >
            ← Назад
          </button>
          <button
            className="btn btn-primary"
            onClick={handleNext}
            disabled={!isAnswerSelected() || analyzing}
            style={{ flex: 1 }}
          >
            {analyzing ? 'Анализируем...' : 
              (currentRoleIndex === scenarios.length - 1 && currentQuestionIndex === currentRole.questions.length - 1
                ? 'Завершить →'
                : 'Далее →')}
          </button>
        </div>
      </div>
    </div>
  )
}
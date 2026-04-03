import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function CareerPath() {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    loadAnalysis()
  }, [])

  async function loadAnalysis() {
    try {
      const result = await api.getAnalysisResult()
      if (result && result.career_path && result.career_path.length > 0) {
        setAnalysis(result)
      } else {
        // Нет анализа — перенаправляем на дашборд
        navigate('/dashboard')
      }
    } catch (err) {
      console.error('Career path error:', err)
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    )
  }

  if (!analysis) {
    return (
      <div>
        <div className="page-header">
          <h1>🚀 Карьерный путь</h1>
          <p>Твой персональный план развития</p>
        </div>
        <div style={{ padding: 16, textAlign: 'center' }}>
          <div style={{ fontSize: '4rem', marginBottom: 16 }}>🗺️</div>
          <h3>Сначала пройди анализ</h3>
          <p className="text-muted" style={{ marginTop: 8 }}>
            На дашборде нажми «Начать AI-анализ» чтобы получить персональный карьерный путь
          </p>
          <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('/dashboard')}>
            На дашборд
          </button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h1>🚀 Карьерный путь</h1>
        <p>Твой персональный план развития</p>
      </div>

      <div style={{ padding: 16 }}>
        {/* Профиль */}
        {analysis.profile_summary && (
          <div className="card">
            <h3>🧠 Твой AI-профиль</h3>
            <p style={{ marginTop: 8, lineHeight: 1.5, color: 'var(--tg-theme-hint-color)' }}>
              {analysis.profile_summary}
            </p>
            {analysis.personality_type && (
              <div style={{ marginTop: 8 }}>
                <span className="tag tag-primary">{analysis.personality_type}</span>
              </div>
            )}
          </div>
        )}

        {/* Шаги карьерного пути */}
        {analysis.career_path && analysis.career_path.length > 0 && (
          <div className="card">
            <h3>📋 План развития</h3>
            <div style={{ marginTop: 16 }}>
              {analysis.career_path.map((step, i) => (
                <div key={i} className="career-step">
                  <div className="career-step-number">{step.step}</div>
                  <div className="career-step-content">
                    <div className="career-step-title">{step.title}</div>
                    {step.duration && (
                      <div className="career-step-duration">⏱️ {step.duration}</div>
                    )}
                    <div className="career-step-desc" style={{ lineHeight: 1.5 }}>{step.description}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Навыки для развития */}
        {analysis.missing_skills && analysis.missing_skills.length > 0 && (
          <div className="card">
            <h3>⚡ Навыки для развития</h3>
            <p className="text-muted text-sm" style={{ marginBottom: 8 }}>
              Эти навыки повысят твоё соответствие вакансиям
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {analysis.missing_skills.map((skill, i) => (
                <span key={i} className="tag" style={{ background: 'rgba(225, 112, 85, 0.15)', color: 'var(--danger)' }}>
                  📚 {skill}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Рекомендации */}
        {analysis.recommendations && analysis.recommendations.length > 0 && (
          <div className="card">
            <h3>💡 Что делать прямо сейчас</h3>
            <div style={{ marginTop: 8 }}>
              {analysis.recommendations.map((rec, i) => (
                <div key={i} style={{
                  display: 'flex',
                  gap: 10,
                  padding: '10px 12px',
                  background: 'var(--tg-theme-secondary-bg-color)',
                  borderRadius: 10,
                  marginBottom: i < analysis.recommendations.length - 1 ? 8 : 0,
                  fontSize: '0.9rem',
                  lineHeight: 1.4,
                }}>
                  <span style={{ fontSize: '1.2rem' }}>{['🎯', '', '💻', '🤝', ''][i] || '•'}</span>
                  <span style={{ flex: 1 }}>{rec}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Подходящие профессии */}
        {analysis.professions && analysis.professions.length > 0 && (
          <div className="card">
            <h3>🎯 Подходящие профессии</h3>
            {analysis.professions.map((prof, i) => (
              <div key={i} className="profession-card" style={{ marginTop: i > 0 ? 12 : 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div className="profession-title">{prof.title}</div>
                  <span className={`vacancy-match ${prof.match_percent >= 70 ? 'vacancy-match-high' : prof.match_percent >= 50 ? 'vacancy-match-medium' : 'vacancy-match-low'}`}>
                    {prof.match_percent}%
                  </span>
                </div>
                <div className="profession-reason" style={{ marginTop: 6 }}>{prof.reason}</div>
                {prof.salary_range && (
                  <div className="profession-salary" style={{ marginTop: 6 }}>💰 {prof.salary_range}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

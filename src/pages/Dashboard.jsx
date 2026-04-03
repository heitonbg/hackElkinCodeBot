import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function Dashboard() {
  const [profile, setProfile] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const profileData = await api.getProfile()
      if (!profileData.exists) {
        // Нет профиля — показываем демо с заглушкой
        setProfile(null)
        setAnalysis(null)
      } else {
        setProfile(profileData.profile)

        const analysisData = await api.getAnalysisResult()
        if (analysisData && analysisData.professions && analysisData.professions.length > 0) {
          setAnalysis(analysisData)
        }
      }
    } catch (err) {
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  async function handleAnalyze() {
    setAnalyzing(true)
    try {
      const result = await api.analyzeCareer()
      if (result && result.status === 'success') {
        setAnalysis(result.analysis)
      } else if (result && result.error) {
        alert(result.error)
      }
    } catch (err) {
      console.error('Analysis error:', err)
      alert('Ошибка анализа. Попробуй ещё раз.')
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
      </div>
    )
  }

  // Демо режим — нет профиля
  if (!profile) {
    return (
      <div>
        <div className="page-header">
          <h1>🧠 AI Career Navigator</h1>
          <p>МТС — твой карьерный навигатор</p>
        </div>

        <div style={{ padding: '16px' }}>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '4rem', marginBottom: 16 }}>👋</div>
            <h2 style={{ marginBottom: 8 }}>Добро пожаловать!</h2>
            <p className="text-muted" style={{ marginBottom: 24, lineHeight: 1.5 }}>
              Пройди онбординг, чтобы получить персональные AI-рекомендации по карьере в МТС
            </p>
            <button
              className="btn btn-primary"
              onClick={() => navigate('/')}
            >
              🚀 Пройти онбординг
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => navigate('/vacancies')}
              style={{ marginTop: 8 }}
            >
              💼 Смотреть вакансии
            </button>
          </div>
        </div>
      </div>
    )
  }

  const skills = profile?.skills || []
  const interests = profile?.interests || []
  const goals = profile?.career_goals || []

  return (
    <div>
      <div className="page-header">
        <h1>📊 Профиль</h1>
        <p>Твоя карьерная панель</p>
      </div>

      <div style={{ padding: '16px' }}>
        {/* Профиль */}
        <div className="card">
          <h3>👤 Твой профиль</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginTop: 12 }}>
            <div>
              <div className="text-muted text-sm">Образование</div>
              <div style={{ fontWeight: 600 }}>{profile?.education || '—'}</div>
            </div>
            <div>
              <div className="text-muted text-sm">Направление</div>
              <div style={{ fontWeight: 600 }}>{profile?.field || '—'}</div>
            </div>
            <div>
              <div className="text-muted text-sm">Опыт</div>
              <div style={{ fontWeight: 600 }}>{profile?.experience || '—'}</div>
            </div>
            <div>
              <div className="text-muted text-sm">Целей</div>
              <div style={{ fontWeight: 600 }}>{goals.length || 0}</div>
            </div>
          </div>
        </div>

        {/* Навыки */}
        {skills.length > 0 && (
          <div className="card">
            <h3>🛠️ Твои навыки</h3>
            <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {skills.map(skill => (
                <span key={skill} className="tag tag-primary">{skill}</span>
              ))}
            </div>
          </div>
        )}

        {/* Интересы */}
        {interests.length > 0 && (
          <div className="card">
            <h3>🎯 Интересы</h3>
            <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {interests.map(int => (
                <span key={int} className="tag">{int}</span>
              ))}
            </div>
          </div>
        )}

        {/* AI Анализ */}
        {!analysis ? (
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 12 }}>🧠</div>
            <h3>Узнай свою идеальную профессию</h3>
            <p className="text-muted" style={{ marginBottom: 16 }}>
              AI проанализирует твой профиль и подберёт подходящие профессии в МТС
            </p>
            <button
              className="btn btn-primary"
              onClick={handleAnalyze}
              disabled={analyzing}
            >
              {analyzing ? (
                <>
                  <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2, marginRight: 8 }} />
                  Анализирую...
                </>
              ) : (
                '🚀 Начать AI-анализ'
              )}
            </button>
          </div>
        ) : (
          <>
            {/* AI Профиль */}
            <div className="card">
              <h3>🧠 AI-профиль</h3>
              <p style={{ marginTop: 8, lineHeight: 1.5, color: 'var(--tg-theme-hint-color)' }}>
                {analysis.profile_summary || '—'}
              </p>
              {analysis.personality_type && (
                <div style={{ marginTop: 12 }}>
                  <span className="tag tag-primary" style={{ fontSize: '0.95rem', padding: '6px 14px' }}>
                    {analysis.personality_type}
                  </span>
                </div>
              )}
              {analysis.strengths && analysis.strengths.length > 0 && (
                <div style={{ marginTop: 12 }}>
                  <div className="text-muted text-sm" style={{ marginBottom: 6 }}>Сильные стороны:</div>
                  {analysis.strengths.map((s, i) => (
                    <span key={i} className="tag" style={{ marginRight: 4, marginBottom: 4 }}>✅ {s}</span>
                  ))}
                </div>
              )}
            </div>

            {/* Профессии */}
            <div className="card">
              <h3>🎯 Подходящие профессии</h3>
              {analysis.professions?.map((prof, i) => (
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

            {/* Навыки для развития */}
            {analysis.missing_skills && analysis.missing_skills.length > 0 && (
              <div className="card">
                <h3>⚡ Чему стоит научиться</h3>
                <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
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
                <h3>💡 Рекомендации</h3>
                <div style={{ marginTop: 8 }}>
                  {analysis.recommendations.map((rec, i) => (
                    <div key={i} style={{
                      padding: '10px 12px',
                      background: 'var(--tg-theme-secondary-bg-color)',
                      borderRadius: 10,
                      marginBottom: i < analysis.recommendations.length - 1 ? 8 : 0,
                      fontSize: '0.9rem',
                      lineHeight: 1.4,
                    }}>
                      {['🎯', '📖', '💻', '🤝', ''][i] || '•'} {rec}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

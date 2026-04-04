import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { api } from '../api/client'

export default function Dashboard() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [matchedRoles, setMatchedRoles] = useState([])
  const [scenarioStats, setScenarioStats] = useState([])
  const [vacancies, setVacancies] = useState([])
  const [vacanciesLoading, setVacanciesLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('стажер')
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const profileData = await api.getProfile()
      if (!profileData.exists) {
        setProfile(null)
      } else {
        setProfile(profileData.profile)

        // 1. Мгновенный rule-based матчинг ролей
        try {
          const rolesResult = await api.matchRoles()
          setMatchedRoles(rolesResult.roles || [])
        } catch (e) {
          console.warn('Role matching failed')
        }

        // 2. Результаты тестирования
        try {
          const stats = await api.getMyScenarioStats()
          setScenarioStats(stats.results || [])
        } catch (e) {
          console.warn('Scenario stats failed')
        }
      }
    } catch (err) {
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  async function searchVacancies() {
    setVacanciesLoading(true)
    try {
      const result = await api.searchVacancies(searchQuery, '', 10)
      setVacancies(result.vacancies || [])
    } catch (e) {
      console.error('Vacancy search failed')
    } finally {
      setVacanciesLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading"><div className="spinner" /></div>
    )
  }

  if (!profile) {
    return (
      <div>
        <div className="page-header">
          <h1>🧠 Career Navigator</h1>
          <p>Твой карьерный навигатор</p>
        </div>
        <div style={{ padding: 16 }}>
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '4rem', marginBottom: 16 }}>👋</div>
            <h2>Добро пожаловать!</h2>
            <p className="text-muted" style={{ marginBottom: 24, lineHeight: 1.5 }}>
              Узнай подходящие роли, пройди тестирование и получи персональный карьерный план
            </p>
            <button className="btn btn-primary" onClick={() => navigate('/role-selection')}>
              🚀 Начать
            </button>
          </div>
        </div>
      </div>
    )
  }

  const rolesTested = new Set(scenarioStats.map(s => s.role_id)).size
  const avgScore = scenarioStats.length > 0
    ? Math.round(scenarioStats.reduce((sum, s) => sum + (s.match_score || 0), 0) / scenarioStats.length)
    : null
  const skills = profile?.skills || []

  return (
    <div>
      <div className="page-header">
        <h1>🚀 Карьерный путь</h1>
        <p>Твой персональный план развития</p>
      </div>

      <div style={{ padding: 16 }}>

        {/* ====== 1. ПОДХОДЯЩИЕ РОЛИ ====== */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <h3 style={{ margin: 0 }}>🎯 Подходящие роли</h3>
            <button
              className="btn btn-primary"
              style={{ padding: '6px 14px', fontSize: '0.8rem' }}
              onClick={() => navigate('/role-selection')}
            >
              + Выбрать ещё
            </button>
          </div>

          {matchedRoles.length > 0 ? (
            matchedRoles.slice(0, 6).map((role, i) => (
              <div key={role.role_id} className="profession-card" style={{ marginTop: i > 0 ? 10 : 0 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div className="profession-title">{role.title}</div>
                  <span className={`vacancy-match ${role.match_percent >= 70 ? 'vacancy-match-high' : role.match_percent >= 50 ? 'vacancy-match-medium' : 'vacancy-match-low'}`}>
                    {role.match_percent}%
                  </span>
                </div>
                <div className="profession-reason" style={{ marginTop: 4 }}>{role.reason}</div>
                <div style={{ marginTop: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>{role.category}</div>
                  <button
                    className="btn btn-secondary"
                    style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                    onClick={() => navigate('/scenario-runner', { state: { roles: [role] } })}
                  >
                    Пройти тест →
                  </button>
                </div>
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: 20 }}>
              <p className="text-muted">Выбери роли для тестирования</p>
              <button className="btn btn-primary" style={{ marginTop: 8 }} onClick={() => navigate('/role-selection')}>
                Выбрать роли
              </button>
            </div>
          )}
        </div>

        {/* ====== 2. РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ====== */}
        {scenarioStats.length > 0 && (
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
              <div style={{
                width: 56, height: 56, borderRadius: '50%',
                background: avgScore >= 70 ? 'rgba(0,184,148,0.15)' : avgScore >= 40 ? 'rgba(253,203,110,0.15)' : 'rgba(225,112,85,0.15)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontWeight: 700, fontSize: '1.1rem',
                color: avgScore >= 70 ? 'var(--success)' : avgScore >= 40 ? '#e17055' : 'var(--danger)',
              }}>
                {avgScore}%
              </div>
              <div>
                <div style={{ fontWeight: 600 }}>Средний балл</div>
                <div className="text-muted text-sm">{rolesTested} ролей пройдено из {matchedRoles.length}</div>
              </div>
            </div>

            {scenarioStats.slice(0, 8).map((stat, i) => (
              <div key={i} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '8px 0',
                borderBottom: i < Math.min(scenarioStats.length, 8) - 1 ? '1px solid var(--tg-theme-secondary-bg-color)' : 'none',
              }}>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{stat.role_id}</div>
                  {stat.feedback && <div className="text-muted text-sm">{stat.feedback}</div>}
                </div>
                <span style={{
                  padding: '4px 10px', borderRadius: 16,
                  background: stat.match_score >= 70 ? 'rgba(0,184,148,0.15)' : stat.match_score >= 40 ? 'rgba(253,203,110,0.15)' : 'rgba(225,112,85,0.15)',
                  color: stat.match_score >= 70 ? 'var(--success)' : stat.match_score >= 40 ? '#e17055' : 'var(--danger)',
                  fontWeight: 700, fontSize: '0.85rem',
                }}>
                  {stat.match_score}%
                </span>
              </div>
            ))}

            <button
              className="btn btn-secondary"
              style={{ width: '100%', marginTop: 12 }}
              onClick={() => navigate('/role-selection')}
            >
              🔄 Пройти заново
            </button>
          </div>
        )}

        {/* ====== 3. НАВЫКИ ====== */}
        {skills.length > 0 && (
          <div className="card">
            <h3>🛠️ Твои навыки</h3>
            <div style={{ marginTop: 8, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
              {skills.map(s => <span key={s} className="tag tag-primary">{s}</span>)}
            </div>
          </div>
        )}

        {/* ====== 4. ПРОФИЛЬ (компактно) ====== */}
        <div className="card">
          <h3>👤 Профиль</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 8, marginTop: 8 }}>
            <div><div className="text-muted text-sm">Образование</div><div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{profile?.education || '—'}</div></div>
            <div><div className="text-muted text-sm">Направление</div><div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{profile?.field || '—'}</div></div>
            <div><div className="text-muted text-sm">Опыт</div><div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{profile?.experience || '—'}</div></div>
          </div>
        </div>

        {/* ====== 5. ВАКАНСИИ HH.RU (второстепенно) ====== */}
        <div className="card">
          <h3>💼 Вакансии на рынке</h3>
          <p className="text-muted text-sm" style={{ marginBottom: 10 }}>Поиск по HH.ru</p>

          <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
            <input
              type="text"
              className="chat-input"
              style={{ flex: 1, borderRadius: 10, padding: '8px 12px', fontSize: '0.85rem' }}
              placeholder="Профессия..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && searchVacancies()}
            />
            <button className="btn btn-primary" style={{ padding: '8px 14px', fontSize: '0.85rem' }} onClick={searchVacancies}>
              🔍
            </button>
          </div>

          {vacanciesLoading && <div className="loading" style={{ padding: 20 }}><div className="spinner" style={{ width: 24, height: 24 }} /></div>}

          {!vacanciesLoading && vacancies.length > 0 && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {vacancies.slice(0, 5).map((v, i) => (
                <a key={v.id || i} href={v.url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', color: 'inherit' }}>
                  <div style={{
                    padding: 10, borderRadius: 10,
                    background: 'var(--tg-theme-secondary-bg-color)',
                    borderLeft: '3px solid var(--primary)',
                  }}>
                    <div style={{ fontWeight: 600, fontSize: '0.85rem' }}>{v.title}</div>
                    <div className="text-muted text-sm">{v.company} • {v.salary || 'По договорённости'}</div>
                  </div>
                </a>
              ))}
            </div>
          )}

          {!vacanciesLoading && vacancies.length === 0 && (
            <div className="text-muted text-sm" style={{ textAlign: 'center', padding: 16 }}>
              Введи профессию и нажми 🔍
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'

export default function CareerPath() {
  const [matchedRoles, setMatchedRoles] = useState([])
  const [scenarioStats, setScenarioStats] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedForTest, setSelectedForTest] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const profileData = await api.getProfile()
      if (!profileData.exists) {
        navigate('/diagnostic')
        return
      }

      // Проверяем, заполнен ли профиль (не просто существует, а есть данные)
      const profile = profileData.profile || {}
      const hasField = profile.field && profile.field.trim().length > 0
      const hasInterests = (profile.interests || []).length > 0
      const hasSkills = (profile.skills || []).length > 0
      const hasGoals = (profile.career_goals || []).length > 0

      // Если профиль пустой или почти пустой — отправляем на диагностику
      if (!hasField && !hasInterests && !hasSkills && !hasGoals) {
        navigate('/diagnostic')
        return
      }

      // Сначала пробуем загрузить результаты диагностики
      const storedResults = localStorage.getItem('diagnostic_results')
      if (storedResults) {
        try {
          const parsed = JSON.parse(storedResults)
          if (parsed.recommended_roles && parsed.recommended_roles.length > 0) {
            setMatchedRoles(parsed.recommended_roles)
            // Статистика сценариев
            const stats = await api.getMyScenarioStats()
            setScenarioStats(stats.results || [])
            setLoading(false)
            return
          }
        } catch (e) {
          console.error('Failed to parse diagnostic results:', e)
        }
      }

      // Fallback: rule-based матчинг
      const rolesResult = await api.matchRoles()
      setMatchedRoles(rolesResult.roles || [])

      // Статистика сценариев
      const stats = await api.getMyScenarioStats()
      setScenarioStats(stats.results || [])
    } catch (err) {
      console.error('CareerPath error:', err)
    } finally {
      setLoading(false)
    }
  }

  const toggleSelect = (role) => {
    setSelectedForTest(prev => {
      const exists = prev.find(r => r.role_id === role.role_id)
      if (exists) return prev.filter(r => r.role_id !== role.role_id)
      return [...prev, role]
    })
  }

  const startTest = () => {
    if (selectedForTest.length === 0) {
      // Если ничего не выбрано — берём топ-3 по совпадению
      const top3 = matchedRoles.filter(r => r.match_percent >= 30).slice(0, 3)
      navigate('/scenario-runner', { state: { roles: top3 } })
    } else {
      navigate('/scenario-runner', { state: { roles: selectedForTest } })
    }
  }

  if (loading) {
    return <div className="loading"><div className="spinner" /></div>
  }

  const testedRoleIds = new Set(scenarioStats.map(s => s.role_id))
  const untestedRoles = matchedRoles.filter(r => !testedRoleIds.has(r.role_id))
  const testedRoles = matchedRoles.filter(r => testedRoleIds.has(r.role_id))

  return (
    <div>
      <div className="page-header">
        <h1>🎯 Выбор ролей</h1>
        <p>Выбери роли для тестирования</p>
      </div>

      <div style={{ padding: 16 }}>

        {/* Непротестированные роли */}
        {untestedRoles.length > 0 && (
          <div className="card">
            <h3>🆕 Доступные роли ({untestedRoles.length})</h3>
            <p className="text-muted text-sm" style={{ marginBottom: 12 }}>
              Выбери одну или несколько — по каждой будет тест
            </p>

            {untestedRoles.slice(0, 15).map((role, i) => (
              <button
                key={role.role_id}
                onClick={() => toggleSelect(role)}
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                  padding: '12px 14px', borderRadius: 10, marginBottom: i < untestedRoles.length - 1 ? 8 : 0,
                  border: selectedForTest.find(r => r.role_id === role.role_id)
                    ? '2px solid var(--primary)'
                    : '2px solid rgba(255,255,255,0.12)',
                  background: selectedForTest.find(r => r.role_id === role.role_id)
                    ? 'rgba(227,6,17,0.1)'
                    : 'rgba(255,255,255,0.04)',
                  cursor: 'pointer', width: '100%', textAlign: 'left',
                }}
              >
                <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{ fontSize: '1.3rem' }}>{role.category_emoji || '💼'}</span>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.95rem' }}>{role.title}</div>
                    <div className="text-muted text-sm">{role.category_emoji || ''} {role.category} • {role.reason}</div>
                  </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{
                    padding: '3px 8px', borderRadius: 12, fontSize: '0.75rem', fontWeight: 700,
                    background: role.match_percent >= 70 ? 'rgba(0,184,148,0.15)' : role.match_percent >= 50 ? 'rgba(253,203,110,0.15)' : 'rgba(225,112,85,0.15)',
                    color: role.match_percent >= 70 ? 'var(--success)' : role.match_percent >= 50 ? '#e17055' : 'var(--danger)',
                  }}>
                    {role.match_percent}%
                  </span>
                  <span style={{
                    width: 20, height: 20, borderRadius: '50%',
                    border: `2px solid ${selectedForTest.find(r => r.role_id === role.role_id) ? 'var(--primary)' : 'rgba(255,255,255,0.25)'}`,
                    background: selectedForTest.find(r => r.role_id === role.role_id) ? 'var(--primary)' : 'transparent',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    color: 'white', fontSize: '0.65rem', fontWeight: 700,
                  }}>
                    {selectedForTest.find(r => r.role_id === role.role_id) && '✓'}
                  </span>
                </div>
              </button>
            ))}
          </div>
        )}

        {/* Протестированные роли */}
        {testedRoles.length > 0 && (
          <div className="card">
            <h3>✅ Пройденные роли ({testedRoles.length})</h3>
            {testedRoles.slice(0, 10).map((role, i) => {
              const stat = scenarioStats.find(s => s.role_id === role.role_id)
              return (
                <div key={role.role_id} style={{
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  padding: '8px 0',
                  borderBottom: i < testedRoles.length - 1 ? '1px solid var(--tg-theme-secondary-bg-color)' : 'none',
                }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{role.title}</div>
                    {stat?.feedback && <div className="text-muted text-sm">{stat.feedback}</div>}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <span style={{
                      padding: '3px 10px', borderRadius: 16, fontSize: '0.8rem', fontWeight: 700,
                      background: stat?.match_score >= 70 ? 'rgba(0,184,148,0.15)' : stat?.match_score >= 40 ? 'rgba(253,203,110,0.15)' : 'rgba(225,112,85,0.15)',
                      color: stat?.match_score >= 70 ? 'var(--success)' : stat?.match_score >= 40 ? '#e17055' : 'var(--danger)',
                    }}>
                      {stat?.match_score}%
                    </span>
                    <button
                      className="btn btn-secondary"
                      style={{ padding: '3px 8px', fontSize: '0.7rem' }}
                      onClick={() => navigate('/scenario-runner', { state: { roles: [role] } })}
                    >
                      ↻
                    </button>
                  </div>
                </div>
              )
            })}
          </div>
        )}

        {/* Кнопка начала теста */}
        <button
          className="btn btn-primary"
          style={{ width: '100%', marginTop: 12 }}
          onClick={startTest}
        >
          🚀 {selectedForTest.length > 0
            ? `Начать тест (${selectedForTest.length} ${selectedForTest.length === 1 ? 'роль' : selectedForTest.length < 5 ? 'роли' : 'ролей'})`
            : 'Начать тест (топ-3 роли)'}
        </button>

      </div>
    </div>
  )
}

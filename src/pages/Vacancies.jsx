import { useState, useEffect } from 'react'
import { api } from '../api/client'

export default function Vacancies() {
  const [mtsVacancies, setMtsVacancies] = useState([])
  const [hhVacancies, setHhVacancies] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState('mts') // 'mts' or 'hh'

  useEffect(() => {
    loadMtsVacancies()
  }, [])

  async function loadMtsVacancies() {
    setLoading(true)
    setActiveTab('mts')
    try {
      const result = await api.getMatchedMtsVacancies(10)
      setMtsVacancies(result.matched_vacancies || [])
    } catch (err) {
      console.error('Load MTS vacancies error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleHhSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return

    setLoading(true)
    setActiveTab('hh')
    try {
      const result = await api.searchVacancies(searchQuery)
      setHhVacancies(result.vacancies || [])
    } catch (err) {
      console.error('HH search error:', err)
    } finally {
      setLoading(false)
    }
  }

  const getMatchLabel = (score) => {
    if (score >= 60) return { text: `${score}% совпадение`, cls: 'vacancy-match-high' }
    if (score >= 30) return { text: `${score}% совпадение`, cls: 'vacancy-match-medium' }
    return { text: `${score}% совпадение`, cls: 'vacancy-match-low' }
  }

  return (
    <div>
      <div className="page-header">
        <h1>💼 Вакансии</h1>
        <p>Карьера в МТС и на рынке</p>
      </div>

      <div style={{ padding: 16 }}>
        {/* Табы */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
          <button
            className={`btn ${activeTab === 'mts' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={loadMtsVacancies}
            style={{ flex: 1 }}
          >
            🏢 Вакансии МТС
          </button>
          <button
            className={`btn ${activeTab === 'hh' ? 'btn-primary' : 'btn-secondary'}`}
            onClick={() => setActiveTab('hh')}
            style={{ flex: 1 }}
          >
            🔍 Поиск на HH.ru
          </button>
        </div>

        {/* Поиск HH */}
        {activeTab === 'hh' && (
          <form onSubmit={handleHhSearch} style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                type="text"
                className="chat-input"
                style={{ flex: 1, borderRadius: 12 }}
                placeholder="Профессия, компания..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button type="submit" className="chat-send-btn" disabled={loading}>
                🔍
              </button>
            </div>
          </form>
        )}

        {/* Загрузка */}
        {loading && (
          <div className="loading">
            <div className="spinner" />
          </div>
        )}

        {/* Вакансии МТС */}
        {!loading && activeTab === 'mts' && mtsVacancies.length > 0 && (
          <>
            <div className="text-muted text-sm" style={{ marginBottom: 12 }}>
              Подобрано {mtsVacancies.length} вакансий МТС под твои навыки
            </div>
            {mtsVacancies.map((item, i) => {
              const v = item.vacancy
              const match = getMatchLabel(item.match_score || 0)
              return (
                <div key={v.id || i} className="vacancy-card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                    <span className={`vacancy-match ${match.cls}`}>{match.text}</span>
                    <span className="text-muted text-sm">{v.level}</span>
                  </div>
                  <div className="vacancy-title">{v.title}</div>
                  <div className="vacancy-company">{v.department} • {v.location}</div>
                  {v.salary && (
                    <div className="vacancy-salary">{v.salary}</div>
                  )}
                  {item.matching_skills?.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <div className="text-muted text-sm" style={{ marginBottom: 4 }}>✅ Твои навыки:</div>
                      {item.matching_skills.slice(0, 4).map((s, j) => (
                        <span key={j} className="tag tag-primary" style={{ marginRight: 4 }}>{s}</span>
                      ))}
                    </div>
                  )}
                  {item.missing_skills?.length > 0 && (
                    <div style={{ marginTop: 8 }}>
                      <div className="text-muted text-sm" style={{ marginBottom: 4 }}>📚 Стоит изучить:</div>
                      {item.missing_skills.slice(0, 3).map((s, j) => (
                        <span key={j} className="tag" style={{ background: 'rgba(225, 112, 85, 0.15)', color: 'var(--danger)', marginRight: 4 }}>{s}</span>
                      ))}
                    </div>
                  )}
                  {item.recommendations?.length > 0 && (
                    <div style={{ marginTop: 8, padding: '8px 12px', background: 'var(--tg-theme-secondary-bg-color)', borderRadius: 8 }}>
                      <div className="text-muted text-sm" style={{ marginBottom: 4 }}>💡 Рекомендации:</div>
                      {item.recommendations.slice(0, 2).map((r, j) => (
                        <div key={j} className="text-sm" style={{ marginBottom: 2 }}>• {r}</div>
                      ))}
                    </div>
                  )}
                  <div style={{ marginTop: 12, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                    {v.requirements?.slice(0, 3).map((req, j) => (
                      <span key={j} className="tag" style={{ fontSize: '0.75rem' }}>{req.slice(0, 50)}{req.length > 50 ? '...' : ''}</span>
                    ))}
                  </div>
                </div>
              )
            })}
          </>
        )}

        {/* Вакансии HH.ru */}
        {!loading && activeTab === 'hh' && hhVacancies.length > 0 && (
          <>
            <div className="text-muted text-sm" style={{ marginBottom: 12 }}>
              Найдено: {hhVacancies.length} вакансий
            </div>
            {hhVacancies.map((vacancy, i) => (
              <a
                key={vacancy.id || i}
                href={vacancy.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{ textDecoration: 'none', color: 'inherit' }}
              >
                <div className="vacancy-card">
                  <div className="vacancy-title">{vacancy.title}</div>
                  <div className="vacancy-company">{vacancy.company}</div>
                  {vacancy.salary && (
                    <div className="vacancy-salary">{vacancy.salary}</div>
                  )}
                  {vacancy.location && (
                    <div className="text-muted text-sm">📍 {vacancy.location}</div>
                  )}
                  {vacancy.description_snippet && (
                    <div className="text-muted text-sm" style={{ marginTop: 8 }}>
                      {vacancy.description_snippet}
                    </div>
                  )}
                  <div style={{ marginTop: 12, fontSize: '0.85rem', color: 'var(--primary)' }}>
                    Открыть на HH.ru →
                  </div>
                </div>
              </a>
            ))}
          </>
        )}

        {/* Нет результатов */}
        {!loading && activeTab === 'mts' && mtsVacancies.length === 0 && (
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 12 }}>🏢</div>
            <h3>Пройди онбординг</h3>
            <p className="text-muted">Заполни профиль, чтобы подобрать вакансии МТС</p>
          </div>
        )}
        {!loading && activeTab === 'hh' && hhVacancies.length === 0 && (
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: 12 }}>😕</div>
            <h3>Ничего не найдено</h3>
            <p className="text-muted">Попробуй другой запрос</p>
          </div>
        )}
      </div>
    </div>
  )
}

import { Link, useLocation } from 'react-router-dom'

export default function BottomNav() {
  const location = useLocation()
  const pathname = location.pathname

  const navItems = [
    { path: '/dashboard', icon: '📊', label: 'Профиль' },
    { path: '/career', icon: '🚀', label: 'Карьера' },
    { path: '/vacancies', icon: '💼', label: 'Вакансии' },
    { path: '/chat', icon: '💬', label: 'Чат' },
  ]

  return (
    <nav className="bottom-nav">
      {navItems.map(item => (
        <Link
          key={item.path}
          to={item.path}
          className={`bottom-nav-item ${pathname === item.path ? 'active' : ''}`}
          style={pathname === item.path ? {
            position: 'relative',
          } : {}}
        >
          <span className="bottom-nav-icon">{item.icon}</span>
          <span>{item.label}</span>
          {pathname === item.path && (
            <div style={{
              position: 'absolute',
              bottom: '-8px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '4px',
              height: '4px',
              borderRadius: '50%',
              background: 'var(--mts-red)',
            }} />
          )}
        </Link>
      ))}
    </nav>
  )
}

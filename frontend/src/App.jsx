import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import CareerPath from './pages/CareerPath'
import Vacancies from './pages/Vacancies'
import Chat from './pages/Chat'
import BottomNav from './components/BottomNav'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path="/" element={<Onboarding />} />
          <Route path="/dashboard" element={<><Dashboard /><BottomNav /></>} />
          <Route path="/career" element={<><CareerPath /><BottomNav /></>} />
          <Route path="/vacancies" element={<><Vacancies /><BottomNav /></>} />
          <Route path="/chat" element={<><Chat /><BottomNav /></>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App

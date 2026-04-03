import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import QuickOnboarding from './pages/QuickOnboarding'
import ScenarioTest from './pages/ScenarioTest'
import Dashboard from './pages/Dashboard'
import CareerPath from './pages/CareerPath'
import Vacancies from './pages/Vacancies'
import Chat from './pages/Chat'
import BottomNav from './components/BottomNav'

function App() {
  const [onboardingDone, setOnboardingDone] = useState(false)
  const [userData, setUserData] = useState(null)
  const [recommendedRoles, setRecommendedRoles] = useState(null)
  console.log('🔄 App: onboardingDone =', onboardingDone, 'recommendedRoles =', recommendedRoles)


  // Если онбординг не пройден — показываем его
  if (!onboardingDone) {
    return (
      <QuickOnboarding 
        onComplete={(answers, analysis) => {
          setUserData(answers)
          setRecommendedRoles(analysis?.professions || [])
          setOnboardingDone(true)
        }} 
      />
    )
  }

  // Если онбординг пройден — показываем сценарии (с выбором ролей)
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <ScenarioTest 
            recommendedRoles={recommendedRoles} 
            userData={userData}
            onComplete={() => setOnboardingDone(false)}
          />
        } />
        <Route path="/dashboard" element={<><Dashboard /><BottomNav /></>} />
        <Route path="/career" element={<><CareerPath /><BottomNav /></>} />
        <Route path="/vacancies" element={<><Vacancies /><BottomNav /></>} />
        <Route path="/chat" element={<><Chat /><BottomNav /></>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
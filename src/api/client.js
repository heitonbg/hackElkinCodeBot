const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function getTelegramId() {
  if (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initDataUnsafe) {
    return String(window.Telegram.WebApp.initDataUnsafe.user?.id || 'demo_user');
  }
  return 'demo_user';
}

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export const api = {
  // User
  async saveOnboarding(data) {
    return request('/user/onboarding', {
      method: 'POST',
      body: JSON.stringify({ ...data, telegram_id: getTelegramId() }),
    });
  },

  async getProfile() {
    return request(`/user/profile/${getTelegramId()}`);
  },

  async getStats() {
    return request(`/user/stats/${getTelegramId()}`);
  },

  // Career
  async analyzeCareer() {
    return request('/career/analyze', {
      method: 'POST',
      body: JSON.stringify({ telegram_id: getTelegramId() }),
    });
  },

  async quickMatch2() {
    return request('/career/quick-match', {
      method: 'POST',
      body: JSON.stringify({ telegram_id: getTelegramId() }),
    });
  },

  async getAnalysisResult() {
    return request(`/career/result/${getTelegramId()}`);
  },

  // Vacancies
  async searchVacancies(profession = '', location = '', limit = 20) {
    return request(`/vacancies/search?profession=${profession}&location=${location}&limit=${limit}`);
  },

  async matchVacancies(profession = '', location = '') {
    return request('/vacancies/match', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: getTelegramId(),
        profession,
        location,
      }),
    });
  },

  // MTS Vacancies
  async getMtsVacancies(onlyIt = true) {
    return request(`/vacancies/mts?only_it=${onlyIt}`);
  },

  async getMatchedMtsVacancies(topN = 10) {
    return request(`/vacancies/mts/match/${getTelegramId()}?top_n=${topN}`);
  },

  // Chat
  async sendMessage(message, context = null) {
    return request('/chat/message', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: getTelegramId(),
        message,
        context,
      }),
    });
  },

  async getChatHistory(limit = 20) {
    return request(`/chat/history/${getTelegramId()}?limit=${limit}`);
  },

  // Scenarios
  async getScenarios() {
    return request('/scenarios/scenarios');
  },

  async analyzeScenario(roleId, answers) {
    return request('/scenarios/analyze', {
      method: 'POST',
      body: JSON.stringify({
        telegram_id: getTelegramId(),
        role_id: roleId,
        answers: answers,
      }),
    });
  },

  async getHhScenarios() {
    return request('/scenarios/hh');
    },
};

export { getTelegramId };
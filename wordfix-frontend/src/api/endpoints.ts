// ─── API Endpoints ─────────────────────────────────────────────────────────────

const API_ENDPOINTS = {
  AUTH: {
    REGISTER: '/auth/register/',
    LOGIN: '/auth/login/',
    LOGOUT: '/auth/logout/',
    REFRESH: '/auth/token/refresh/',
    PROFILE: '/auth/profile/',
    CHANGE_PASSWORD: '/auth/change-password/',
  },
  WORDS: {
    LIST: '/words/',
    DETAIL: (id: string) => `/words/${id}/`,
    BULK: '/words/bulk/',
    STATS: '/words/stats/',
    REVIEW: '/words/review/',
    CATEGORIES: '/words/categories/',
    CATEGORY_DETAIL: (id: string) => `/words/categories/${id}/`,
    ENRICH: (id: string) => `/words/${id}/enrich/`,
    ENRICHMENT_STATUS: '/words/enrichment-status/',
  },
  REVIEW: {
    WORDS: '/review/words/',
    SESSIONS: '/review/sessions/',
    SESSION_DETAIL: (id: string) => `/review/sessions/${id}/`,
    SESSION_SUBMIT: (id: string) => `/review/sessions/${id}/submit/`,
    SESSION_COMPLETE: (id: string) => `/review/sessions/${id}/complete/`,
    SUMMARY: '/review/summary/',
    STREAK: '/review/streak/',
    DAILY_PROGRESS: '/review/daily-progress/',
  },
  TESTS: {
    GENERATE: '/tests/generate/',
    HISTORY: '/tests/history/',
    DETAIL: (id: string) => `/tests/${id}/`,
    ANSWER: (id: string) => `/tests/${id}/answer/`,
    COMPLETE: (id: string) => `/tests/${id}/complete/`,
  },
  GAMES: {
    SPEED_ROUND_START: '/games/speed-round/start/',
    SPEED_ROUND_SUBMIT: '/games/speed-round/submit/',
    WORD_MATCH_START: '/games/word-match/start/',
    WORD_MATCH_SUBMIT: '/games/word-match/submit/',
    WORD_CONTEXT_START: '/games/word-context/start/',
    WORD_CONTEXT_SUBMIT: '/games/word-context/submit/',
    HISTORY: '/games/history/',
    STATS: '/games/stats/',
  },
  PROGRESS: {
    USER_PROGRESS: '/users/progress/',
    XP_HISTORY: '/users/xp-history/',
    USER_BADGES: '/users/badges/',
    ALL_BADGES: '/badges/',
  },
  NOTIFICATIONS: {
    LIST: '/notifications/',
    MARK_READ: '/notifications/read/',
    UNREAD_COUNT: '/notifications/unread-count/',
  },
} as const;

export default API_ENDPOINTS;

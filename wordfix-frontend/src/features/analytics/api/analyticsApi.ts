import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  AnalyticsOverview,
  ApiResponse,
  CalendarDay,
  DailyStatsEntry,
  DifficultWord,
  WordProgressData,
} from '@/types';

export const analyticsApi = {
  getOverview: async () => {
    const res = await apiClient.get<ApiResponse<AnalyticsOverview>>(
      API_ENDPOINTS.ANALYTICS.OVERVIEW,
    );
    return res.data;
  },

  getWeekly: async () => {
    const res = await apiClient.get<ApiResponse<DailyStatsEntry[]>>(
      API_ENDPOINTS.ANALYTICS.WEEKLY,
    );
    return res.data;
  },

  getMonthly: async () => {
    const res = await apiClient.get<ApiResponse<DailyStatsEntry[]>>(
      API_ENDPOINTS.ANALYTICS.MONTHLY,
    );
    return res.data;
  },

  getDifficultWords: async () => {
    const res = await apiClient.get<ApiResponse<DifficultWord[]>>(
      API_ENDPOINTS.ANALYTICS.DIFFICULT_WORDS,
    );
    return res.data;
  },

  getWordProgress: async () => {
    const res = await apiClient.get<ApiResponse<WordProgressData>>(
      API_ENDPOINTS.ANALYTICS.WORD_PROGRESS,
    );
    return res.data;
  },

  getCalendar: async (year?: number, month?: number) => {
    const params = new URLSearchParams();
    if (year) params.set('year', String(year));
    if (month) params.set('month', String(month));
    const res = await apiClient.get<ApiResponse<CalendarDay[]>>(
      `${API_ENDPOINTS.ANALYTICS.CALENDAR}?${params.toString()}`,
    );
    return res.data;
  },
};

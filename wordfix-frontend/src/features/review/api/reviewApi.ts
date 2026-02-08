import apiClient from '@/api/client';
import type {
  ApiResponse,
  DailyProgress,
  DailyStreak,
  EnrichmentStatusResponse,
  PredictedIntervals,
  ReviewAnswer,
  ReviewAnswerResult,
  ReviewSession,
  ReviewSummary,
  SessionType,
  Word,
} from '@/types';

// ─── Review API ────────────────────────────────────────────────────────────────

export const reviewApi = {
  getReviewWords: async (type: SessionType = 'review', limit = 20) => {
    const params = new URLSearchParams({ type, limit: String(limit) });
    const res = await apiClient.get<ApiResponse<Word[]>>(
      `/review/words/?${params.toString()}`,
    );
    return res.data;
  },

  startSession: async (sessionType: SessionType = 'review') => {
    const res = await apiClient.post<ApiResponse<ReviewSession>>(
      '/review/sessions/',
      { session_type: sessionType },
    );
    return res.data;
  },

  getSession: async (sessionId: string) => {
    const res = await apiClient.get<ApiResponse<ReviewSession>>(
      `/review/sessions/${sessionId}/`,
    );
    return res.data;
  },

  submitAnswer: async (sessionId: string, answer: ReviewAnswer) => {
    const res = await apiClient.post<ApiResponse<ReviewAnswerResult>>(
      `/review/sessions/${sessionId}/submit/`,
      answer,
    );
    return res.data;
  },

  completeSession: async (sessionId: string) => {
    const res = await apiClient.post<ApiResponse<ReviewSession>>(
      `/review/sessions/${sessionId}/complete/`,
    );
    return res.data;
  },

  getSummary: async () => {
    const res = await apiClient.get<ApiResponse<ReviewSummary>>(
      '/review/summary/',
    );
    return res.data;
  },

  getHistory: async (page = 1, pageSize = 10) => {
    const params = new URLSearchParams({
      page: String(page),
      page_size: String(pageSize),
    });
    const res = await apiClient.get<ApiResponse<ReviewSession[]>>(
      `/review/history/?${params.toString()}`,
    );
    return res.data;
  },

  getStreak: async () => {
    const res = await apiClient.get<ApiResponse<DailyStreak>>(
      '/review/streak/',
    );
    return res.data;
  },

  getDailyProgress: async () => {
    const res = await apiClient.get<ApiResponse<DailyProgress>>(
      '/review/daily-progress/',
    );
    return res.data;
  },

  getPredictedIntervals: async (wordId: string) => {
    const res = await apiClient.get<ApiResponse<PredictedIntervals>>(
      `/review/words/${wordId}/predict/`,
    );
    return res.data;
  },
};

// ─── Enrichment API ────────────────────────────────────────────────────────────

export const enrichmentApi = {
  enrichWord: async (wordId: string) => {
    const res = await apiClient.post<ApiResponse>(
      `/words/${wordId}/enrich/`,
    );
    return res.data;
  },

  enrichAll: async () => {
    const res = await apiClient.post<ApiResponse<{ count: number }>>(
      '/words/enrich-all/',
    );
    return res.data;
  },

  getStatus: async (wordId: string) => {
    const res = await apiClient.get<ApiResponse<EnrichmentStatusResponse>>(
      `/words/${wordId}/enrichment-status/`,
    );
    return res.data;
  },
};

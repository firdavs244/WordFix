import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  GameSession,
  GameStats,
  SpeedRoundAnswer,
  SpeedRoundStartResponse,
  WordContextAnswer,
  WordContextStartResponse,
  WordMatchPair,
  WordMatchStartResponse,
} from '@/types';

export const gameApi = {
  // Speed Round
  startSpeedRound: async () => {
    const res = await apiClient.post<ApiResponse<SpeedRoundStartResponse>>(
      API_ENDPOINTS.GAMES.SPEED_ROUND_START,
    );
    return res.data;
  },

  submitSpeedRound: async (sessionId: string, answers: SpeedRoundAnswer[], durationSeconds = 60) => {
    const res = await apiClient.post<ApiResponse<GameSession>>(
      API_ENDPOINTS.GAMES.SPEED_ROUND_SUBMIT,
      { session_id: sessionId, answers, duration_seconds: durationSeconds },
    );
    return res.data;
  },

  // Word Match
  startWordMatch: async (pairCount = 8) => {
    const res = await apiClient.post<ApiResponse<WordMatchStartResponse>>(
      API_ENDPOINTS.GAMES.WORD_MATCH_START,
      { pair_count: pairCount },
    );
    return res.data;
  },

  submitWordMatch: async (sessionId: string, pairs: WordMatchPair[], timeSeconds: number) => {
    const res = await apiClient.post<ApiResponse<GameSession>>(
      API_ENDPOINTS.GAMES.WORD_MATCH_SUBMIT,
      { session_id: sessionId, pairs, time_seconds: timeSeconds },
    );
    return res.data;
  },

  // Word Context
  startWordContext: async () => {
    const res = await apiClient.post<ApiResponse<WordContextStartResponse>>(
      API_ENDPOINTS.GAMES.WORD_CONTEXT_START,
    );
    return res.data;
  },

  submitWordContext: async (sessionId: string, answers: WordContextAnswer[]) => {
    const res = await apiClient.post<ApiResponse<GameSession>>(
      API_ENDPOINTS.GAMES.WORD_CONTEXT_SUBMIT,
      { session_id: sessionId, answers },
    );
    return res.data;
  },

  // History & Stats
  getHistory: async (page = 1, pageSize = 20) => {
    const params = new URLSearchParams({
      page: String(page),
      page_size: String(pageSize),
    });
    const res = await apiClient.get<ApiResponse<GameSession[]>>(
      `${API_ENDPOINTS.GAMES.HISTORY}?${params.toString()}`,
    );
    return res.data;
  },

  getStats: async () => {
    const res = await apiClient.get<ApiResponse<GameStats>>(
      API_ENDPOINTS.GAMES.STATS,
    );
    return res.data;
  },
};

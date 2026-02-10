import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { ApiResponse } from '@/types';
import type { DailyChallenges } from '../types';

// ─── Challenge API ─────────────────────────────────────────────────────────────

export const challengeApi = {
  getToday: async () => {
    const res = await apiClient.get<ApiResponse<DailyChallenges>>(
      API_ENDPOINTS.CHALLENGES.TODAY,
    );
    return res.data;
  },

  claimBonus: async () => {
    const res = await apiClient.post<ApiResponse<{ xp_earned: number }>>(
      API_ENDPOINTS.CHALLENGES.CLAIM,
    );
    return res.data;
  },
};

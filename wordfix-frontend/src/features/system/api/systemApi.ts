import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { ApiResponse, SystemHealth, ConfigStatus, AIStatusResponse } from '@/types';

// ─── System API ────────────────────────────────────────────────────────────────

export const systemApi = {
  getDetailedHealth: async () => {
    const res = await apiClient.get<ApiResponse<SystemHealth>>(
      API_ENDPOINTS.SYSTEM.HEALTH,
    );
    return res.data;
  },

  getConfigStatus: async () => {
    const res = await apiClient.get<ApiResponse<ConfigStatus>>(
      API_ENDPOINTS.SYSTEM.CONFIG,
    );
    return res.data;
  },

  getAIStatus: async () => {
    const res = await apiClient.get<ApiResponse<AIStatusResponse>>(
      API_ENDPOINTS.SYSTEM.AI_STATUS,
    );
    return res.data;
  },
};

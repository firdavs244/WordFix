import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { ApiResponse } from '@/types';
import type { ConfusingPair, ConfusingPairsCountResponse, DrillData } from '../types';

// ─── Confusing Pairs API ───────────────────────────────────────────────────────

export const confusingApi = {
  getList: async () => {
    const res = await apiClient.get<ApiResponse<ConfusingPair[]>>(
      API_ENDPOINTS.CONFUSING_PAIRS.LIST,
    );
    return res.data;
  },

  getDetail: async (id: string) => {
    const res = await apiClient.get<ApiResponse<ConfusingPair>>(
      API_ENDPOINTS.CONFUSING_PAIRS.DETAIL(id),
    );
    return res.data;
  },

  generateDrill: async (id: string) => {
    const res = await apiClient.post<ApiResponse<DrillData>>(
      API_ENDPOINTS.CONFUSING_PAIRS.DRILL(id),
    );
    return res.data;
  },

  resolve: async (id: string) => {
    const res = await apiClient.post<ApiResponse<ConfusingPair>>(
      API_ENDPOINTS.CONFUSING_PAIRS.RESOLVE(id),
    );
    return res.data;
  },

  getUnresolvedCount: async () => {
    const res = await apiClient.get<ApiResponse<ConfusingPairsCountResponse>>(
      API_ENDPOINTS.CONFUSING_PAIRS.COUNT,
    );
    return res.data;
  },
};

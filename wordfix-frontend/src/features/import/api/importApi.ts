import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  AnalyzeTextRequest,
  AnalyzeTextResponse,
  ApiResponse,
  ImportWordsRequest,
  ImportWordsResponse,
} from '@/types';

export const importApi = {
  analyzeText: async (data: AnalyzeTextRequest) => {
    const res = await apiClient.post<ApiResponse<AnalyzeTextResponse>>(
      API_ENDPOINTS.IMPORT.ANALYZE,
      data,
    );
    return res.data;
  },

  addWords: async (data: ImportWordsRequest) => {
    const res = await apiClient.post<ApiResponse<ImportWordsResponse>>(
      API_ENDPOINTS.IMPORT.ADD,
      data,
    );
    return res.data;
  },
};

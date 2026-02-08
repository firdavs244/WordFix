import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  TestAnswerRequest,
  TestAnswerResponse,
  TestDetailResponse,
  TestGenerateRequest,
  TestGenerateResponse,
  TestSession,
} from '@/types';

export const testApi = {
  generate: async (data: TestGenerateRequest) => {
    const res = await apiClient.post<ApiResponse<TestGenerateResponse>>(
      API_ENDPOINTS.TESTS.GENERATE,
      data,
    );
    return res.data;
  },

  submitAnswer: async (sessionId: string, data: TestAnswerRequest) => {
    const res = await apiClient.post<ApiResponse<TestAnswerResponse>>(
      API_ENDPOINTS.TESTS.ANSWER(sessionId),
      data,
    );
    return res.data;
  },

  complete: async (sessionId: string) => {
    const res = await apiClient.post<ApiResponse<TestSession>>(
      API_ENDPOINTS.TESTS.COMPLETE(sessionId),
    );
    return res.data;
  },

  getDetail: async (sessionId: string) => {
    const res = await apiClient.get<ApiResponse<TestDetailResponse>>(
      API_ENDPOINTS.TESTS.DETAIL(sessionId),
    );
    return res.data;
  },

  getHistory: async (page = 1, pageSize = 20) => {
    const params = new URLSearchParams({
      page: String(page),
      page_size: String(pageSize),
    });
    const res = await apiClient.get<ApiResponse<TestSession[]>>(
      `${API_ENDPOINTS.TESTS.HISTORY}?${params.toString()}`,
    );
    return res.data;
  },
};

import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  LearningProfile,
  AnalyzeResult,
  MistakePattern,
  WordRecommendation,
  DomainCoverage,
  DifficultyInfo,
} from '@/types';

// ─── Learning API ──────────────────────────────────────────────────────────────

export const learningApi = {
  getLearningProfile: async () => {
    const res = await apiClient.get<ApiResponse<LearningProfile>>(
      API_ENDPOINTS.LEARNING.PROFILE,
    );
    return res.data;
  },

  analyzeLearningProfile: async () => {
    const res = await apiClient.post<ApiResponse<AnalyzeResult>>(
      API_ENDPOINTS.LEARNING.ANALYZE,
    );
    return res.data;
  },

  getMistakePatterns: async () => {
    const res = await apiClient.get<ApiResponse<MistakePattern[]>>(
      API_ENDPOINTS.LEARNING.MISTAKES,
    );
    return res.data;
  },

  getWordRecommendations: async () => {
    const res = await apiClient.get<ApiResponse<WordRecommendation[]>>(
      API_ENDPOINTS.LEARNING.RECOMMENDATIONS,
    );
    return res.data;
  },

  acceptRecommendation: async (recommendationId: string) => {
    const res = await apiClient.post<ApiResponse<{ recommendation_id: string }>>(
      API_ENDPOINTS.LEARNING.RECOMMENDATIONS,
      { recommendation_id: recommendationId },
    );
    return res.data;
  },

  getDomainCoverage: async () => {
    const res = await apiClient.get<ApiResponse<DomainCoverage>>(
      API_ENDPOINTS.LEARNING.DOMAIN_COVERAGE,
    );
    return res.data;
  },

  getDifficulty: async () => {
    const res = await apiClient.get<ApiResponse<DifficultyInfo>>(
      API_ENDPOINTS.LEARNING.DIFFICULTY,
    );
    return res.data;
  },
};

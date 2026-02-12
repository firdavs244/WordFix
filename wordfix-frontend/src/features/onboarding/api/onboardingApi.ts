import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { ApiResponse } from '@/types';
import type {
  OnboardingQuestion,
  OnboardingAnswer,
  OnboardingResult,
  OnboardingStatus,
} from '../types';

// ─── Onboarding API ───────────────────────────────────────────────────────────

export const onboardingApi = {
  getQuestions: async () => {
    const res = await apiClient.get<
      ApiResponse<{ questions: OnboardingQuestion[] }>
    >(API_ENDPOINTS.ONBOARDING.QUESTIONS);
    return res.data;
  },

  submit: async (answers: OnboardingAnswer[]) => {
    const res = await apiClient.post<ApiResponse<OnboardingResult>>(
      API_ENDPOINTS.ONBOARDING.SUBMIT,
      { answers },
    );
    return res.data;
  },

  skip: async () => {
    const res = await apiClient.post<ApiResponse<OnboardingResult>>(
      API_ENDPOINTS.ONBOARDING.SKIP,
    );
    return res.data;
  },

  getStatus: async () => {
    const res = await apiClient.get<ApiResponse<OnboardingStatus>>(
      API_ENDPOINTS.ONBOARDING.STATUS,
    );
    return res.data;
  },
};

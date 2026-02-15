import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  TestGenerateRequest,
  TestGenerateResponse,
  TestAnswerRequest,
  TestAnswerResponse,
  TestSession,
  TestDetailResponse,
} from '@/types';

export function useGenerateTest() {
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  return useMutation({
    mutationFn: async (config: TestGenerateRequest) => {
      const { data } = await apiClient.post<{ data: TestGenerateResponse }>(
        API_ENDPOINTS.TESTS.GENERATE,
        config,
      );
      return data.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['tests', 'history'] });
      navigate(`/tests/session/${data.session.id}`, { state: { questions: data.questions } });
    },
    onError: () => toast.error('Failed to generate test. Please try again.'),
  });
}

export function useTestSession(sessionId: string) {
  return useQuery({
    queryKey: ['tests', sessionId],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: TestDetailResponse }>(
        API_ENDPOINTS.TESTS.DETAIL(sessionId),
      );
      return data.data;
    },
    enabled: !!sessionId,
  });
}

export function useSubmitTestAnswer(sessionId: string) {
  return useMutation({
    mutationFn: async (answer: TestAnswerRequest) => {
      const { data } = await apiClient.post<{ data: TestAnswerResponse }>(
        API_ENDPOINTS.TESTS.ANSWER(sessionId),
        answer,
      );
      return data.data;
    },
  });
}

export function useCompleteTest() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (sessionId: string) => {
      const { data } = await apiClient.post<{ data: TestSession }>(
        API_ENDPOINTS.TESTS.COMPLETE(sessionId),
      );
      return data.data;
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tests'] }),
  });
}

export function useRecentTests() {
  return useQuery({
    queryKey: ['tests', 'history'],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: TestSession[] }>(API_ENDPOINTS.TESTS.HISTORY);
      return data.data;
    },
  });
}

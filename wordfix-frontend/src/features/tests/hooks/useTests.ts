import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { testApi } from '../api/testApi';
import type { TestAnswerRequest, TestGenerateRequest } from '@/types';
import { toast } from 'sonner';

export const testKeys = {
  all: ['tests'] as const,
  history: (page?: number) => [...testKeys.all, 'history', page] as const,
  detail: (id: string) => [...testKeys.all, 'detail', id] as const,
};

export function useTestHistory(page = 1) {
  return useQuery({
    queryKey: testKeys.history(page),
    queryFn: () => testApi.getHistory(page),
  });
}

export function useTestDetail(sessionId: string) {
  return useQuery({
    queryKey: testKeys.detail(sessionId),
    queryFn: () => testApi.getDetail(sessionId),
    enabled: !!sessionId,
  });
}

export function useGenerateTest() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TestGenerateRequest) => testApi.generate(data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: testKeys.all });
    },
    onError: () => {
      toast.error('Failed to generate test. Please try again.');
    },
  });
}

export function useSubmitTestAnswer() {
  return useMutation({
    mutationFn: ({ sessionId, data }: { sessionId: string; data: TestAnswerRequest }) =>
      testApi.submitAnswer(sessionId, data),
  });
}

export function useCompleteTest() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (sessionId: string) => testApi.complete(sessionId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: testKeys.all });
    },
  });
}

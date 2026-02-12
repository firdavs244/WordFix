import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { onboardingApi } from '../api/onboardingApi';
import type { OnboardingAnswer } from '../types';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const onboardingKeys = {
  all: ['onboarding'] as const,
  questions: () => [...onboardingKeys.all, 'questions'] as const,
  status: () => [...onboardingKeys.all, 'status'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useOnboardingQuestions() {
  return useQuery({
    queryKey: onboardingKeys.questions(),
    queryFn: () => onboardingApi.getQuestions(),
    staleTime: 1000 * 60 * 30, // 30 mins — questions rarely change
  });
}

export function useOnboardingStatus() {
  return useQuery({
    queryKey: onboardingKeys.status(),
    queryFn: () => onboardingApi.getStatus(),
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useSubmitOnboarding() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (answers: OnboardingAnswer[]) => onboardingApi.submit(answers),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
    onError: () => {
      toast.error('Failed to submit answers. Please try again.');
    },
  });
}

export function useSkipOnboarding() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => onboardingApi.skip(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
    onError: () => {
      toast.error('Failed to skip onboarding.');
    },
  });
}

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { reviewApi, enrichmentApi } from '../api/reviewApi';
import type { ReviewAnswer, SessionType } from '@/types';
import { toast } from 'sonner';
import { wordKeys } from '@/features/words/hooks/useWords';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const reviewKeys = {
  all: ['review'] as const,
  reviewWords: (type?: SessionType) => [...reviewKeys.all, 'words', type] as const,
  sessions: () => [...reviewKeys.all, 'sessions'] as const,
  session: (id: string) => [...reviewKeys.sessions(), id] as const,
  summary: () => [...reviewKeys.all, 'summary'] as const,
  history: (page?: number) => [...reviewKeys.all, 'history', page] as const,
  streak: () => [...reviewKeys.all, 'streak'] as const,
  dailyProgress: () => [...reviewKeys.all, 'daily-progress'] as const,
  predict: (wordId: string) => [...reviewKeys.all, 'predict', wordId] as const,
  enrichmentStatus: (wordId: string) => [...reviewKeys.all, 'enrichment', wordId] as const,
};

// ─── Review Queries ────────────────────────────────────────────────────────────

export function useReviewWords(type: SessionType = 'review', limit = 20) {
  return useQuery({
    queryKey: reviewKeys.reviewWords(type),
    queryFn: () => reviewApi.getReviewWords(type, limit),
  });
}

export function useReviewSession(sessionId: string) {
  return useQuery({
    queryKey: reviewKeys.session(sessionId),
    queryFn: () => reviewApi.getSession(sessionId),
    enabled: !!sessionId,
  });
}

export function useReviewSummary() {
  return useQuery({
    queryKey: reviewKeys.summary(),
    queryFn: () => reviewApi.getSummary(),
  });
}

export function useReviewHistory(page = 1, pageSize = 10) {
  return useQuery({
    queryKey: reviewKeys.history(page),
    queryFn: () => reviewApi.getHistory(page, pageSize),
  });
}

export function useStreak() {
  return useQuery({
    queryKey: reviewKeys.streak(),
    queryFn: () => reviewApi.getStreak(),
  });
}

export function useDailyProgress() {
  return useQuery({
    queryKey: reviewKeys.dailyProgress(),
    queryFn: () => reviewApi.getDailyProgress(),
  });
}

export function usePredictedIntervals(wordId: string) {
  return useQuery({
    queryKey: reviewKeys.predict(wordId),
    queryFn: () => reviewApi.getPredictedIntervals(wordId),
    enabled: !!wordId,
  });
}

export function useEnrichmentStatus(wordId: string) {
  return useQuery({
    queryKey: reviewKeys.enrichmentStatus(wordId),
    queryFn: () => enrichmentApi.getStatus(wordId),
    enabled: !!wordId,
    refetchInterval: (query) => {
      const status = query.state.data?.data?.enrichment_status;
      return status === 'processing' ? 3000 : false;
    },
  });
}

// ─── Review Mutations ──────────────────────────────────────────────────────────

export function useStartSession() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionType: SessionType) => reviewApi.startSession(sessionType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewKeys.sessions() });
    },
    onError: () => {
      toast.error('Failed to start review session.');
    },
  });
}

export function useSubmitAnswer(sessionId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (answer: ReviewAnswer) => reviewApi.submitAnswer(sessionId, answer),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewKeys.session(sessionId) });
      queryClient.invalidateQueries({ queryKey: reviewKeys.dailyProgress() });
    },
    onError: () => {
      toast.error('Failed to submit answer.');
    },
  });
}

export function useCompleteSession() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionId: string) => reviewApi.completeSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: reviewKeys.all });
      queryClient.invalidateQueries({ queryKey: wordKeys.all });
      toast.success('Review session completed!');
    },
    onError: () => {
      toast.error('Failed to complete session.');
    },
  });
}

export function useEnrichWord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (wordId: string) => enrichmentApi.enrichWord(wordId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.all });
      toast.success('Word enrichment started!');
    },
    onError: () => {
      toast.error('Failed to enrich word.');
    },
  });
}

export function useEnrichAll() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => enrichmentApi.enrichAll(),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: wordKeys.all });
      toast.success(`Enrichment started for ${data.data.count} words!`);
    },
    onError: () => {
      toast.error('Failed to start batch enrichment.');
    },
  });
}

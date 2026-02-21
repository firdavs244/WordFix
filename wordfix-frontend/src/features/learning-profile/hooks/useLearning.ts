import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { learningApi } from '../api/learningApi';
import { wordKeys } from '@/features/words/hooks/useWords';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const learningKeys = {
  all: ['learning'] as const,
  profile: () => [...learningKeys.all, 'profile'] as const,
  mistakes: () => [...learningKeys.all, 'mistakes'] as const,
  recommendations: () => [...learningKeys.all, 'recommendations'] as const,
  domainCoverage: () => [...learningKeys.all, 'domain-coverage'] as const,
  difficulty: () => [...learningKeys.all, 'difficulty'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useLearningProfile() {
  return useQuery({
    queryKey: learningKeys.profile(),
    queryFn: () => learningApi.getLearningProfile(),
  });
}

export function useMistakePatterns() {
  return useQuery({
    queryKey: learningKeys.mistakes(),
    queryFn: () => learningApi.getMistakePatterns(),
  });
}

export function useWordRecommendations() {
  return useQuery({
    queryKey: learningKeys.recommendations(),
    queryFn: () => learningApi.getWordRecommendations(),
  });
}

export function useDomainCoverage() {
  return useQuery({
    queryKey: learningKeys.domainCoverage(),
    queryFn: () => learningApi.getDomainCoverage(),
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useAnalyzeProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => learningApi.analyzeLearningProfile(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: learningKeys.profile() });
      queryClient.invalidateQueries({ queryKey: learningKeys.recommendations() });
      queryClient.invalidateQueries({ queryKey: learningKeys.mistakes() });
      queryClient.invalidateQueries({ queryKey: learningKeys.domainCoverage() });
      toast.success('Profil muvaffaqiyatli tahlil qilindi!');
    },
    onError: () => {
      toast.error('Tahlil qilishda xatolik yuz berdi.');
    },
  });
}

export function useAcceptRecommendation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (recommendationId: string) =>
      learningApi.acceptRecommendation(recommendationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: learningKeys.recommendations() });
      queryClient.invalidateQueries({ queryKey: wordKeys.all });
      toast.success("So'z lug'atga qo'shildi!");
    },
    onError: () => {
      toast.error("So'zni qo'shishda xatolik yuz berdi.");
    },
  });
}

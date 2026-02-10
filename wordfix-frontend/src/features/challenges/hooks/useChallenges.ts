import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { challengeApi } from '../api/challengeApi';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const challengeKeys = {
  all: ['daily-challenges'] as const,
  today: () => [...challengeKeys.all, 'today'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useDailyChallenges() {
  return useQuery({
    queryKey: challengeKeys.today(),
    queryFn: () => challengeApi.getToday(),
    staleTime: 30_000,
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useClaimBonus() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => challengeApi.claimBonus(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: challengeKeys.all });
      toast.success('Daily bonus claimed! +50 XP');
    },
    onError: () => {
      toast.error('Failed to claim bonus.');
    },
  });
}

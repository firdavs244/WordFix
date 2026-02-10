import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { gameApi } from '../api/gameApi';
import type { SpeedRoundAnswer, WordContextAnswer, WordMatchPair } from '@/types';
import { toast } from 'sonner';

export const gameKeys = {
  all: ['games'] as const,
  history: (page?: number) => [...gameKeys.all, 'history', page] as const,
  stats: () => [...gameKeys.all, 'stats'] as const,
};

export function useGameHistory(page = 1) {
  return useQuery({
    queryKey: gameKeys.history(page),
    queryFn: () => gameApi.getHistory(page),
  });
}

export function useGameStats() {
  return useQuery({
    queryKey: gameKeys.stats(),
    queryFn: () => gameApi.getStats(),
  });
}

export function useStartSpeedRound() {
  return useMutation<Awaited<ReturnType<typeof gameApi.startSpeedRound>>, Error, void>({
    mutationFn: () => gameApi.startSpeedRound(),
    onError: () => toast.error('Failed to start Speed Round.'),
  });
}

export function useSubmitSpeedRound() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ sessionId, answers, duration }: { sessionId: string; answers: SpeedRoundAnswer[]; duration: number }) =>
      gameApi.submitSpeedRound(sessionId, answers, duration),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: gameKeys.all });
      qc.invalidateQueries({ queryKey: ['daily-challenges'] });
    },
  });
}

export function useStartWordMatch() {
  return useMutation({
    mutationFn: (pairCount?: number) => gameApi.startWordMatch(pairCount),
    onError: () => toast.error('Failed to start Word Match.'),
  });
}

export function useSubmitWordMatch() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ sessionId, pairs, timeSeconds }: { sessionId: string; pairs: WordMatchPair[]; timeSeconds: number }) =>
      gameApi.submitWordMatch(sessionId, pairs, timeSeconds),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: gameKeys.all });
      qc.invalidateQueries({ queryKey: ['daily-challenges'] });
    },
  });
}

export function useStartWordContext() {
  return useMutation<Awaited<ReturnType<typeof gameApi.startWordContext>>, Error, void>({
    mutationFn: () => gameApi.startWordContext(),
    onError: () => toast.error('Failed to start Word Context.'),
  });
}

export function useSubmitWordContext() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ sessionId, answers }: { sessionId: string; answers: WordContextAnswer[] }) =>
      gameApi.submitWordContext(sessionId, answers),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: gameKeys.all });
      qc.invalidateQueries({ queryKey: ['daily-challenges'] });
    },
  });
}

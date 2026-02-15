import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { GameStats } from '@/types';

export function useGameStats() {
  return useQuery({
    queryKey: ['games', 'stats'],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: GameStats }>(API_ENDPOINTS.GAMES.STATS);
      return data.data;
    },
  });
}

export function useGameHistory() {
  return useQuery({
    queryKey: ['games', 'history'],
    queryFn: async () => {
      const { data } = await apiClient.get<{ data: import('@/types').GameSession[] }>(API_ENDPOINTS.GAMES.HISTORY);
      return data.data;
    },
  });
}

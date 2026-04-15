/**
 * Hook for fetching immersive scenarios.
 */

import { useQuery } from '@tanstack/react-query';
import { immersiveApi } from '../api/immersiveApi';

export function useScenarios(params?: { difficulty?: string; location?: string }) {
  return useQuery({
    queryKey: ['immersive-scenarios', params],
    queryFn: () => immersiveApi.getScenarios(params),
  });
}

export function useScenarioDetail(id: string) {
  return useQuery({
    queryKey: ['immersive-scenario', id],
    queryFn: () => immersiveApi.getScenarioDetail(id),
    enabled: !!id,
  });
}

import { useQuery } from '@tanstack/react-query';
import { systemApi } from '../api/systemApi';
import { useAuthStore } from '@/stores/useAuthStore';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const systemKeys = {
  all: ['system'] as const,
  health: () => [...systemKeys.all, 'health'] as const,
  config: () => [...systemKeys.all, 'config'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useSystemHealth() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  return useQuery({
    queryKey: systemKeys.health(),
    queryFn: () => systemApi.getDetailedHealth(),
    enabled: isAuthenticated,
    refetchInterval: 60000,
    staleTime: 30000,
    retry: 1,
  });
}

export function useConfigStatus() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  return useQuery({
    queryKey: systemKeys.config(),
    queryFn: () => systemApi.getConfigStatus(),
    enabled: isAuthenticated,
    staleTime: 60000,
  });
}

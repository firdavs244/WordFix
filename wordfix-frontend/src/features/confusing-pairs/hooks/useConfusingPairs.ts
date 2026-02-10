import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { confusingApi } from '../api/confusingApi';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const confusingPairKeys = {
  all: ['confusing-pairs'] as const,
  list: () => [...confusingPairKeys.all, 'list'] as const,
  detail: (id: string) => [...confusingPairKeys.all, 'detail', id] as const,
  count: () => ['confusing-pairs-count'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useConfusingPairs() {
  return useQuery({
    queryKey: confusingPairKeys.list(),
    queryFn: () => confusingApi.getList(),
  });
}

export function useConfusingPairDetail(id: string) {
  return useQuery({
    queryKey: confusingPairKeys.detail(id),
    queryFn: () => confusingApi.getDetail(id),
    enabled: !!id,
  });
}

export function useUnresolvedCount() {
  return useQuery({
    queryKey: confusingPairKeys.count(),
    queryFn: () => confusingApi.getUnresolvedCount(),
    staleTime: 60_000,
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useGenerateDrill() {
  return useMutation({
    mutationFn: (id: string) => confusingApi.generateDrill(id),
    onError: () => {
      toast.error('Failed to generate drill. Please try again.');
    },
  });
}

export function useResolvePair() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => confusingApi.resolve(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: confusingPairKeys.all });
      queryClient.invalidateQueries({ queryKey: confusingPairKeys.count() });
      toast.success('Pair marked as resolved!');
    },
    onError: () => {
      toast.error('Failed to resolve pair.');
    },
  });
}

import { useMutation, useQueryClient } from '@tanstack/react-query';
import { importApi } from '../api/importApi';
import type { AnalyzeTextRequest, ImportWordsRequest } from '@/types';
import { toast } from 'sonner';
import { wordKeys } from '@/features/words/hooks/useWords';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const importKeys = {
  all: ['import'] as const,
};

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useAnalyzeText() {
  return useMutation({
    mutationFn: (data: AnalyzeTextRequest) => importApi.analyzeText(data),
    onError: () => {
      toast.error('Failed to analyze text. Please try again.');
    },
  });
}

export function useImportWords() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ImportWordsRequest) => importApi.addWords(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: wordKeys.lists() });
      queryClient.invalidateQueries({ queryKey: wordKeys.stats() });
      const result = data.data;
      toast.success(`Imported ${result.created} words! (${result.skipped} skipped)`);
    },
    onError: () => {
      toast.error('Failed to import words.');
    },
  });
}

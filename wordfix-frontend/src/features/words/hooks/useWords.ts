import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { wordsApi } from '../api/wordApi';
import type { WordCreateData, WordFilters, WordUpdateData } from '@/types';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const wordKeys = {
  all: ['words'] as const,
  lists: () => [...wordKeys.all, 'list'] as const,
  list: (filters?: WordFilters) => [...wordKeys.lists(), filters] as const,
  details: () => [...wordKeys.all, 'detail'] as const,
  detail: (id: string) => [...wordKeys.details(), id] as const,
  stats: () => [...wordKeys.all, 'stats'] as const,
  review: () => [...wordKeys.all, 'review'] as const,
  categories: () => [...wordKeys.all, 'categories'] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useWords(filters?: WordFilters) {
  return useQuery({
    queryKey: wordKeys.list(filters),
    queryFn: () => wordsApi.list(filters),
  });
}

export function useWord(id: string) {
  return useQuery({
    queryKey: wordKeys.detail(id),
    queryFn: () => wordsApi.getById(id),
    enabled: !!id,
  });
}

export function useWordStats() {
  return useQuery({
    queryKey: wordKeys.stats(),
    queryFn: () => wordsApi.getStats(),
  });
}

export function useReviewWords() {
  return useQuery({
    queryKey: wordKeys.review(),
    queryFn: () => wordsApi.getReviewWords(),
  });
}

export function useCategories() {
  return useQuery({
    queryKey: wordKeys.categories(),
    queryFn: () => wordsApi.listCategories(),
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useCreateWord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: WordCreateData) => wordsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.lists() });
      queryClient.invalidateQueries({ queryKey: wordKeys.stats() });
      queryClient.invalidateQueries({ queryKey: ['daily-challenges'] });
      toast.success('Word added successfully!');
    },
    onError: () => {
      toast.error('Failed to add word.');
    },
  });
}

export function useUpdateWord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: WordUpdateData }) =>
      wordsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.all });
      toast.success('Word updated!');
    },
    onError: () => {
      toast.error('Failed to update word.');
    },
  });
}

export function useDeleteWord() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => wordsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.lists() });
      queryClient.invalidateQueries({ queryKey: wordKeys.stats() });
      toast.success('Word deleted.');
    },
    onError: () => {
      toast.error('Failed to delete word.');
    },
  });
}

export function useBulkCreateWords() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (words: WordCreateData[]) => wordsApi.bulkCreate({ words }),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: wordKeys.lists() });
      queryClient.invalidateQueries({ queryKey: wordKeys.stats() });
      const result = data.data;
      toast.success(`Created ${result.created} words, skipped ${result.skipped}.`);
    },
    onError: () => {
      toast.error('Bulk create failed.');
    },
  });
}

export function useCreateCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { name: string; color?: string; icon?: string }) =>
      wordsApi.createCategory(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.categories() });
      toast.success('Category created!');
    },
    onError: () => {
      toast.error('Failed to create category.');
    },
  });
}

export function useDeleteCategory() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => wordsApi.deleteCategory(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: wordKeys.categories() });
      queryClient.invalidateQueries({ queryKey: wordKeys.lists() });
      toast.success('Category deleted.');
    },
    onError: () => {
      toast.error('Failed to delete category.');
    },
  });
}

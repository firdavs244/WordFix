import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { importApi } from '../api/importApi';
import { toast } from 'sonner';
import type { WordSuggestion } from '@/types';

export function useTextImport() {
  const queryClient = useQueryClient();
  const [text, setText] = useState('');
  const [suggestions, setSuggestions] = useState<WordSuggestion[]>([]);
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [importedCount, setImportedCount] = useState(0);

  const analyzeMutation = useMutation({
    mutationFn: () => importApi.analyzeText({ text }),
    onSuccess: (res) => {
      const s = res.data.suggestions;
      setSuggestions(s);
      setSelectedIds(new Set(s.map((_, i) => i)));
    },
    onError: () => toast.error('Failed to analyze text'),
  });

  const importMutation = useMutation({
    mutationFn: () => {
      const words = suggestions.filter((_, i) => selectedIds.has(i)).map((w) => ({
        original_word: w.word, translation: w.translation,
        part_of_speech: w.part_of_speech, difficulty_level: w.difficulty,
        context_sentence: w.context_sentence,
      }));
      return importApi.addWords({ words });
    },
    onSuccess: (res) => {
      setImportedCount(res.data.created);
      queryClient.invalidateQueries({ queryKey: ['words'] });
      toast.success(`Imported ${res.data.created} words!`);
    },
    onError: () => toast.error('Failed to import words'),
  });

  const toggle = useCallback((i: number) => {
    setSelectedIds((prev) => { const s = new Set(prev); s.has(i) ? s.delete(i) : s.add(i); return s; });
  }, []);

  const selectAll = useCallback(() => setSelectedIds(new Set(suggestions.map((_, i) => i))), [suggestions]);
  const deselectAll = useCallback(() => setSelectedIds(new Set()), []);
  const reset = useCallback(() => { setText(''); setSuggestions([]); setSelectedIds(new Set()); setImportedCount(0); }, []);

  return {
    text, setText, suggestions, selectedIds, importedCount,
    isAnalyzing: analyzeMutation.isPending, isImporting: importMutation.isPending,
    analyze: () => analyzeMutation.mutateAsync(), importSelected: () => importMutation.mutateAsync(),
    toggle, selectAll, deselectAll, reset,
  };
}

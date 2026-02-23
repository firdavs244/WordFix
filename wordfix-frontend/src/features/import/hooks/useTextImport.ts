import { useState, useCallback, useMemo } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { importApi } from '../api/importApi';
import { toast } from 'sonner';
import type { WordSuggestion, DifficultyLevel } from '@/types';

export function useTextImport() {
  const queryClient = useQueryClient();
  const [text, setText] = useState('');
  const [suggestions, setSuggestions] = useState<WordSuggestion[]>([]);
  const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
  const [importedCount, setImportedCount] = useState(0);
  const [parseMode, setParseMode] = useState<string>('');
  const [textDifficulty, setTextDifficulty] = useState<string>('');
  const [alreadyInLibrary, setAlreadyInLibrary] = useState(0);
  const [newWords, setNewWords] = useState(0);
  const [skippedNonEnglish, setSkippedNonEnglish] = useState(0);
  const [aiUsed, setAiUsed] = useState(false);
  const [levelFilter, setLevelFilter] = useState<string>('all');
  const [showOnlyNew, setShowOnlyNew] = useState(false);

  const analyzeMutation = useMutation({
    mutationFn: () => importApi.analyzeText({ text }),
    onSuccess: (res) => {
      const data = res.data;
      const s = data.suggestions || [];
      setSuggestions(s);
      // Auto-deselect words already in library
      const newSelected = new Set<number>();
      s.forEach((w, i) => {
        if (!w.in_user_library) newSelected.add(i);
      });
      setSelectedIds(newSelected);
      setParseMode(data.parse_mode || '');
      setTextDifficulty(data.text_difficulty || '');
      setAlreadyInLibrary(data.already_in_library || 0);
      setNewWords(data.new_words ?? (s.length - (data.already_in_library || 0)));
      setSkippedNonEnglish(data.skipped_non_english || 0);
      setAiUsed(data.ai_used ?? false);
    },
    onError: () => toast.error('Failed to analyze text'),
  });

  const importMutation = useMutation({
    mutationFn: () => {
      const words = suggestions.filter((_, i) => selectedIds.has(i)).map((w) => ({
        original_word: w.word, translation: w.translation,
        part_of_speech: w.part_of_speech, difficulty_level: w.difficulty as DifficultyLevel,
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

  const filteredSuggestions = useMemo(() => {
    let filtered = suggestions;
    if (showOnlyNew) {
      filtered = filtered.filter((w) => !w.in_user_library);
    }
    if (levelFilter === 'all') return filtered;
    return filtered.filter((w) => {
      const d = (w.difficulty || '').toUpperCase();
      if (levelFilter === 'A') return d === 'A1' || d === 'A2';
      if (levelFilter === 'B') return d === 'B1' || d === 'B2';
      if (levelFilter === 'C') return d === 'C1' || d === 'C2';
      return true;
    });
  }, [suggestions, levelFilter, showOnlyNew]);

  const toggle = useCallback((i: number) => {
    setSelectedIds((prev) => { const s = new Set(prev); s.has(i) ? s.delete(i) : s.add(i); return s; });
  }, []);

  const selectAll = useCallback(() => setSelectedIds(new Set(suggestions.map((_, i) => i))), [suggestions]);
  const deselectAll = useCallback(() => setSelectedIds(new Set()), []);
  const selectAllNew = useCallback(() => {
    setSelectedIds(new Set(suggestions.map((w, i) => (!w.in_user_library ? i : -1)).filter((i) => i >= 0)));
  }, [suggestions]);
  const deselectLibrary = useCallback(() => {
    setSelectedIds((prev) => {
      const s = new Set(prev);
      suggestions.forEach((w, i) => { if (w.in_user_library) s.delete(i); });
      return s;
    });
  }, [suggestions]);
  const reset = useCallback(() => { setText(''); setSuggestions([]); setSelectedIds(new Set()); setImportedCount(0); setParseMode(''); setTextDifficulty(''); setAlreadyInLibrary(0); setNewWords(0); setSkippedNonEnglish(0); setAiUsed(false); setLevelFilter('all'); setShowOnlyNew(false); }, []);

  return {
    text, setText, suggestions, filteredSuggestions, selectedIds, importedCount,
    parseMode, textDifficulty, alreadyInLibrary, newWords, skippedNonEnglish, aiUsed,
    levelFilter, setLevelFilter, showOnlyNew, setShowOnlyNew,
    isAnalyzing: analyzeMutation.isPending, isImporting: importMutation.isPending,
    analyze: () => analyzeMutation.mutateAsync(), importSelected: () => importMutation.mutateAsync(),
    toggle, selectAll, deselectAll, selectAllNew, deselectLibrary, reset,
  };
}

import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { WordMatchStartResponse, GameSession } from '@/types';

interface MatchPair {
  wordId: string;
  word: string;
  translation: string;
  matched: boolean;
}

interface MatchedTranslation {
  text: string;
  matched: boolean;
}

export function useWordMatch() {
  const [phase, setPhase] = useState<'ready' | 'playing' | 'complete'>('ready');
  const [sessionId, setSessionId] = useState('');
  const [pairs, setPairs] = useState<MatchPair[]>([]);
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [selectedTranslation, setSelectedTranslation] = useState<string | null>(null);
  const [wrongPair, setWrongPair] = useState<{ word: string; translation: string } | null>(null);
  const [combo, setCombo] = useState(0);
  const [translations, setTranslations] = useState<MatchedTranslation[]>([]);
  const [startTime, setStartTime] = useState<number>(0);

  const startMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: WordMatchStartResponse }>(API_ENDPOINTS.GAMES.WORD_MATCH_START);
      return data.data;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      // Use the correct translation from each word (backend now includes it)
      const wordItems = data.words as Array<{ word_id: string; word: string; translation?: string }>;
      const correctPairs = wordItems.map((w, i) => ({
        wordId: w.word_id,
        word: w.word,
        translation: w.translation || data.translations[i],
        matched: false,
      }));
      setPairs(correctPairs);
      // Shuffle translations for display
      const shuffled = [...data.translations].sort(() => Math.random() - 0.5);
      setTranslations(shuffled.map(t => ({ text: t, matched: false })));
      setStartTime(Date.now());
      setPhase('playing');
    },
  });

  const submitMutation = useMutation({
    mutationFn: async () => {
      const elapsed = Math.round((Date.now() - startTime) / 1000);
      const { data } = await apiClient.post<{ data: GameSession }>(
        API_ENDPOINTS.GAMES.WORD_MATCH_SUBMIT,
        {
          session_id: sessionId,
          pairs: pairs.map((p) => ({ word_id: p.wordId, matched_translation: p.translation })),
          time_seconds: elapsed,
        },
      );
      return data.data;
    },
  });

  const selectWord = useCallback((word: string) => {
    setSelectedWord(word);
    if (selectedTranslation) {
      // Check if this word's correct translation matches the selected translation
      const pair = pairs.find((p) => p.word === word && !p.matched);
      if (pair && pair.translation === selectedTranslation) {
        // Correct match!
        setPairs((ps) => ps.map((p) => p.word === word ? { ...p, matched: true } : p));
        setTranslations((ts) => ts.map((t) => t.text === selectedTranslation ? { ...t, matched: true } : t));
        setCombo((c) => c + 1);
        setSelectedWord(null);
        setSelectedTranslation(null);
        const allMatched = pairs.filter((p) => p.word !== word).every((p) => p.matched);
        if (allMatched) { setPhase('complete'); submitMutation.mutate(); }
      } else {
        // Wrong match
        setWrongPair({ word, translation: selectedTranslation });
        setCombo(0);
        setTimeout(() => { setWrongPair(null); setSelectedWord(null); setSelectedTranslation(null); }, 600);
      }
    }
  }, [selectedTranslation, pairs, submitMutation]);

  const selectTranslation = useCallback((translation: string) => {
    setSelectedTranslation(translation);
    if (selectedWord) {
      // Check if selected word's correct translation matches this translation
      const pair = pairs.find((p) => p.word === selectedWord && !p.matched);
      if (pair && pair.translation === translation) {
        // Correct match!
        setPairs((ps) => ps.map((p) => p.word === selectedWord ? { ...p, matched: true } : p));
        setTranslations((ts) => ts.map((t) => t.text === translation ? { ...t, matched: true } : t));
        setCombo((c) => c + 1);
        setSelectedWord(null);
        setSelectedTranslation(null);
        const allMatched = pairs.filter((p) => p.word !== selectedWord).every((p) => p.matched);
        if (allMatched) { setPhase('complete'); submitMutation.mutate(); }
      } else {
        // Wrong match
        setWrongPair({ word: selectedWord, translation });
        setCombo(0);
        setTimeout(() => { setWrongPair(null); setSelectedWord(null); setSelectedTranslation(null); }, 600);
      }
    }
  }, [selectedWord, pairs, submitMutation]);

  return {
    phase, pairs, translations, selectedWord, selectedTranslation, wrongPair, combo,
    start: () => startMutation.mutate(), isStarting: startMutation.isPending,
    selectWord, selectTranslation, result: submitMutation.data,
  };
}

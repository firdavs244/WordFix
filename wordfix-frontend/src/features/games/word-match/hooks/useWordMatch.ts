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

export function useWordMatch() {
  const [phase, setPhase] = useState<'ready' | 'playing' | 'complete'>('ready');
  const [sessionId, setSessionId] = useState('');
  const [pairs, setPairs] = useState<MatchPair[]>([]);
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [selectedTranslation, setSelectedTranslation] = useState<string | null>(null);
  const [wrongPair, setWrongPair] = useState<{ word: string; translation: string } | null>(null);
  const [combo, setCombo] = useState(0);
  const [translations, setTranslations] = useState<string[]>([]);

  const startMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: WordMatchStartResponse }>(API_ENDPOINTS.GAMES.WORD_MATCH_START);
      return data.data;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      setTranslations([...data.translations].sort(() => Math.random() - 0.5));
      setPairs(data.words.map((w, i) => ({
        wordId: w.word_id, word: w.word, translation: data.translations[i], matched: false,
      })));
      setPhase('playing');
    },
  });

  const submitMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: GameSession }>(
        API_ENDPOINTS.GAMES.WORD_MATCH_SUBMIT,
        { session_id: sessionId, matches: pairs.map((p) => ({ word_id: p.wordId, matched_translation: p.translation })) },
      );
      return data.data;
    },
  });

  const selectWord = useCallback((word: string) => {
    setSelectedWord(word);
    if (selectedTranslation) {
      const pair = pairs.find((p) => p.word === word && p.translation === selectedTranslation);
      if (pair) {
        setPairs((ps) => ps.map((p) => p.word === word ? { ...p, matched: true } : p));
        setCombo((c) => c + 1);
        setSelectedWord(null);
        setSelectedTranslation(null);
        const allMatched = pairs.filter((p) => p.word !== word).every((p) => p.matched);
        if (allMatched) { setPhase('complete'); submitMutation.mutate(); }
      } else {
        setWrongPair({ word, translation: selectedTranslation });
        setCombo(0);
        setTimeout(() => { setWrongPair(null); setSelectedWord(null); setSelectedTranslation(null); }, 600);
      }
    }
  }, [selectedTranslation, pairs, submitMutation]);

  const selectTranslation = useCallback((translation: string) => {
    setSelectedTranslation(translation);
    if (selectedWord) {
      const pair = pairs.find((p) => p.word === selectedWord && p.translation === translation);
      if (pair) {
        setPairs((ps) => ps.map((p) => p.word === selectedWord ? { ...p, matched: true } : p));
        setCombo((c) => c + 1);
        setSelectedWord(null);
        setSelectedTranslation(null);
        const allMatched = pairs.filter((p) => p.word !== selectedWord).every((p) => p.matched);
        if (allMatched) { setPhase('complete'); submitMutation.mutate(); }
      } else {
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

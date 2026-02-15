import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { SpeedRoundStartResponse, SpeedRoundWord, GameSession } from '@/types';

export type Phase = 'ready' | 'countdown' | 'playing' | 'complete';

interface SpeedRoundState {
  phase: Phase;
  sessionId: string;
  words: SpeedRoundWord[];
  timeLimit: number;
  currentIndex: number;
  score: number;
  combo: number;
  answers: { wordId: string; correct: boolean }[];
}

export function useSpeedRound() {
  const [state, setState] = useState<SpeedRoundState>({
    phase: 'ready', sessionId: '', words: [], timeLimit: 60,
    currentIndex: 0, score: 0, combo: 0, answers: [],
  });

  const startMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: SpeedRoundStartResponse }>(API_ENDPOINTS.GAMES.SPEED_ROUND_START);
      return data.data;
    },
    onSuccess: (data) => {
      setState((s) => ({
        ...s, sessionId: data.session_id, words: data.words,
        timeLimit: data.time_limit, phase: 'countdown',
      }));
    },
  });

  const submitMutation = useMutation({
    mutationFn: async (answers: { word_id: string; selected_answer: string }[]) => {
      const { data } = await apiClient.post<{ data: GameSession }>(
        API_ENDPOINTS.GAMES.SPEED_ROUND_SUBMIT,
        { session_id: state.sessionId, answers },
      );
      return data.data;
    },
  });

  const start = useCallback(() => startMutation.mutate(), [startMutation]);

  const onCountdownDone = useCallback(() => {
    setState((s) => ({ ...s, phase: 'playing' }));
  }, []);

  const answerWord = useCallback((wordId: string, _selected: string, correct: boolean) => {
    setState((s) => {
      const answers = [...s.answers, { wordId, correct }];
      const combo = correct ? s.combo + 1 : 0;
      const next = s.currentIndex + 1;
      return { ...s, answers, combo, currentIndex: next, score: s.score + (correct ? 10 : 0) };
    });
  }, []);

  const endGame = useCallback(async () => {
    setState((s) => ({ ...s, phase: 'complete' }));
    const answers = state.words.slice(0, state.answers.length).map((w, i) => ({
      word_id: w.word_id,
      selected_answer: state.answers[i]?.correct ? w.correct_translation : '',
    }));
    return submitMutation.mutateAsync(answers);
  }, [state, submitMutation]);

  const current = state.words[state.currentIndex] ?? null;

  return {
    ...state, current, start, onCountdownDone, answerWord, endGame,
    isStarting: startMutation.isPending, result: submitMutation.data,
  };
}

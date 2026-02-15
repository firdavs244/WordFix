import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { ListeningStartResponse, ListeningAnswerResponse, ListeningCompleteResponse } from '@/types';

interface RoundData {
  roundNumber: number;
  audioUrl: string;
  hint: string;
  maxAttempts: number;
}

export function useListening() {
  const [phase, setPhase] = useState<'ready' | 'playing' | 'complete'>('ready');
  const [sessionId, setSessionId] = useState('');
  const [round, setRound] = useState<RoundData | null>(null);
  const [totalRounds, setTotalRounds] = useState(5);
  const [attemptsRemaining, setAttemptsRemaining] = useState(3);
  const [answered, setAnswered] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [combo, setCombo] = useState(0);

  const startMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: ListeningStartResponse }>(API_ENDPOINTS.GAMES.LISTENING_START);
      return data.data;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      setTotalRounds(data.total_rounds);
      setRound({
        roundNumber: data.first_word.round_number,
        audioUrl: data.first_word.audio_url,
        hint: data.first_word.hint,
        maxAttempts: data.first_word.max_attempts,
      });
      setAttemptsRemaining(data.first_word.max_attempts);
      setPhase('playing');
    },
  });

  const answerMutation = useMutation({
    mutationFn: async (answer: string) => {
      const { data } = await apiClient.post<{ data: ListeningAnswerResponse }>(
        API_ENDPOINTS.GAMES.LISTENING_ANSWER,
        { session_id: sessionId, answer, round_number: round?.roundNumber },
      );
      return data.data;
    },
  });

  const completeMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: ListeningCompleteResponse }>(
        API_ENDPOINTS.GAMES.LISTENING_COMPLETE,
        { session_id: sessionId },
      );
      return data.data;
    },
  });

  const submitAnswer = useCallback(async (answer: string) => {
    const res = await answerMutation.mutateAsync(answer);
    setCorrectAnswer(res.correct_answer);
    setAttemptsRemaining(res.attempts_remaining);
    if (res.is_correct) {
      setIsCorrect(true);
      setAnswered(true);
      setCombo(res.combo);
    } else if (res.attempts_remaining <= 0) {
      setAnswered(true);
      setIsCorrect(false);
      setCombo(0);
    }
    return res;
  }, [answerMutation, round]);

  const nextRound = useCallback(async (res?: ListeningAnswerResponse) => {
    const nextData = res?.next_round;
    if (nextData) {
      setRound({ roundNumber: nextData.round_number, audioUrl: nextData.audio_url, hint: nextData.hint, maxAttempts: nextData.max_attempts });
      setAttemptsRemaining(nextData.max_attempts);
      setAnswered(false);
      setIsCorrect(false);
      setCorrectAnswer('');
    } else {
      const result = await completeMutation.mutateAsync();
      setPhase('complete');
      return result;
    }
  }, [completeMutation]);

  return {
    phase, round, totalRounds, attemptsRemaining, answered, isCorrect, correctAnswer, combo,
    start: () => startMutation.mutate(), isStarting: startMutation.isPending,
    submitAnswer, nextRound, result: completeMutation.data,
  };
}

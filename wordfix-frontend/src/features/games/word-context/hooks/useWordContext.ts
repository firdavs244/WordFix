import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { WordContextStartResponse, WordContextQuestion, GameSession } from '@/types';

export function useWordContext() {
  const [phase, setPhase] = useState<'ready' | 'playing' | 'complete'>('ready');
  const [sessionId, setSessionId] = useState('');
  const [questions, setQuestions] = useState<WordContextQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [userAnswer, setUserAnswer] = useState('');
  const [isCorrect, setIsCorrect] = useState(false);
  const [combo, setCombo] = useState(0);
  const [answers, setAnswers] = useState<{ word_id: string; selected_answer: string }[]>([]);

  const startMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: WordContextStartResponse }>(API_ENDPOINTS.GAMES.WORD_CONTEXT_START);
      return data.data;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      setQuestions(data.questions);
      setPhase('playing');
    },
  });

  const submitMutation = useMutation({
    mutationFn: async (a: { word_id: string; selected_answer: string }[]) => {
      const { data } = await apiClient.post<{ data: GameSession }>(
        API_ENDPOINTS.GAMES.WORD_CONTEXT_SUBMIT,
        { session_id: sessionId, answers: a },
      );
      return data.data;
    },
  });

  const current = questions[currentIndex] ?? null;

  const submitAnswer = useCallback((answer: string) => {
    if (!current || answered) return;
    const correct = answer.toLowerCase().trim() === current.correct_answer.toLowerCase().trim();
    setAnswered(true);
    setUserAnswer(answer);
    setIsCorrect(correct);
    setCombo(correct ? (c) => c + 1 : 0);
    setAnswers((a) => [...a, { word_id: current.word_id, selected_answer: answer }]);
  }, [current, answered]);

  const next = useCallback(() => {
    if (currentIndex >= questions.length - 1) {
      setPhase('complete');
      submitMutation.mutate(answers);
    } else {
      setCurrentIndex((i) => i + 1);
      setAnswered(false);
      setUserAnswer('');
      setIsCorrect(false);
    }
  }, [currentIndex, questions.length, answers, submitMutation]);

  return {
    phase, current, currentIndex, total: questions.length,
    answered, userAnswer, isCorrect, combo,
    start: () => startMutation.mutate(), isStarting: startMutation.isPending,
    submitAnswer, next, result: submitMutation.data,
  };
}

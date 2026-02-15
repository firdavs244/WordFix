import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type { StoryStartResponse, StorySubmitResponse, StoryCompleteResponse } from '@/types';

export type StoryPhase = 'genre' | 'playing' | 'complete';

export function useStoryBuilder() {
  const [phase, setPhase] = useState<StoryPhase>('genre');
  const [sessionId, setSessionId] = useState('');
  const [aiText, setAiText] = useState('');
  const [targetWords, setTargetWords] = useState<string[]>([]);
  const [round, setRound] = useState(1);
  const [totalRounds, setTotalRounds] = useState(3);
  const [roundScore, setRoundScore] = useState<number | null>(null);
  const [roundFeedback, setRoundFeedback] = useState('');
  const [totalScore, setTotalScore] = useState(0);
  const [fullStory, setFullStory] = useState('');
  const [combo, setCombo] = useState(0);

  const startMutation = useMutation({
    mutationFn: async (genre: string) => {
      const { data } = await apiClient.post<{ data: StoryStartResponse }>(
        API_ENDPOINTS.GAMES.STORY_BUILDER_START, { genre },
      );
      return data.data;
    },
    onSuccess: (data) => {
      setSessionId(data.session_id);
      setAiText(data.ai_text);
      setTargetWords(data.target_words);
      setTotalRounds(data.total_rounds);
      setRound(data.current_round);
      setPhase('playing');
    },
  });

  const submitMutation = useMutation({
    mutationFn: async (text: string) => {
      const { data } = await apiClient.post<{ data: StorySubmitResponse }>(
        API_ENDPOINTS.GAMES.STORY_BUILDER_SUBMIT,
        { session_id: sessionId, user_text: text, round_number: round },
      );
      return data.data;
    },
    onSuccess: (data) => {
      setRoundScore(data.round_result.score);
      setRoundFeedback(data.round_result.feedback);
      setTotalScore(data.session_stats.total_score);
      setCombo(data.combo);
      if (data.next_round) {
        setTimeout(() => {
          setAiText(data.next_round!.ai_text);
          setTargetWords(data.next_round!.target_words);
          setRound(data.next_round!.round_number);
          setRoundScore(null);
          setRoundFeedback('');
        }, 2000);
      }
    },
  });

  const completeMutation = useMutation({
    mutationFn: async () => {
      const { data } = await apiClient.post<{ data: StoryCompleteResponse }>(
        API_ENDPOINTS.GAMES.STORY_BUILDER_COMPLETE,
        { session_id: sessionId },
      );
      return data.data;
    },
    onSuccess: (data) => {
      setFullStory(data.full_story);
      setTotalScore(data.total_score);
      setPhase('complete');
    },
  });

  const selectGenre = useCallback((genre: string) => startMutation.mutate(genre), [startMutation]);
  const submitText = useCallback((text: string) => submitMutation.mutate(text), [submitMutation]);
  const complete = useCallback(() => completeMutation.mutate(), [completeMutation]);

  return {
    phase, aiText, targetWords, round, totalRounds, roundScore, roundFeedback,
    totalScore, fullStory, combo, selectGenre, submitText, complete,
    isStarting: startMutation.isPending, isSubmitting: submitMutation.isPending,
    result: completeMutation.data,
  };
}

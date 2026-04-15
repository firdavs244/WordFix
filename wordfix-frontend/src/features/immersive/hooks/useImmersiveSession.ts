/**
 * Hook for immersive game session state and mutations.
 */

import { useState, useCallback } from 'react';
import { useMutation } from '@tanstack/react-query';
import { immersiveApi } from '../api/immersiveApi';
import type {
  ConversationTurn,
  HintResponse,
  ImmersiveSessionStart,
  SubmitResponseResult,
  SessionCompleteResult,
} from '../types/immersive';

export type SessionPhase = 'selecting' | 'playing' | 'completing' | 'result';

export function useImmersiveSession() {
  const [phase, setPhase] = useState<SessionPhase>('selecting');
  const [sessionData, setSessionData] = useState<ImmersiveSessionStart | null>(null);
  const [turns, setTurns] = useState<ConversationTurn[]>([]);
  const [totalScore, setTotalScore] = useState(0);
  const [turnCount, setTurnCount] = useState(0);
  const [maxTurns, setMaxTurns] = useState(8);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [lastHint, setLastHint] = useState<HintResponse | null>(null);
  const [result, setResult] = useState<SessionCompleteResult | null>(null);

  const startMutation = useMutation({
    mutationFn: async ({ scenarioId, inputMode }: { scenarioId: string; inputMode?: string }) => {
      return immersiveApi.startSession(scenarioId, inputMode);
    },
    onSuccess: (data) => {
      setSessionData(data);
      setTurns([data.first_turn]);
      setMaxTurns(data.scenario.max_turns);
      setPhase('playing');
    },
  });

  const respondMutation = useMutation({
    mutationFn: async (message: string) => {
      if (!sessionData) throw new Error('No active session');
      return immersiveApi.submitResponse(sessionData.session_id, message);
    },
    onSuccess: (data: SubmitResponseResult) => {
      // Add user turn (from analysis)
      const userTurn: ConversationTurn = {
        turn_number: turns.length + 1,
        role: 'user',
        content: '', // Set by the component
        grammar_errors: data.user_analysis.grammar_errors,
        vocabulary_feedback: data.user_analysis.vocabulary_feedback,
        score: data.user_analysis.score,
        hint_level_used: 0,
      };
      const newTurns = [...turns, userTurn];

      // Add NPC response turn
      if (data.npc_response) {
        const npcTurn: ConversationTurn = {
          turn_number: turns.length + 2,
          role: 'npc',
          content: data.npc_response.content,
          audio_url: data.npc_response.audio_url,
          grammar_errors: [],
          vocabulary_feedback: [],
          score: 0,
          hint_level_used: 0,
        };
        newTurns.push(npcTurn);
      }

      setTurns(newTurns);
      setTotalScore((prev) => prev + data.user_analysis.score);
      setTurnCount(data.session_stats.turn_count);

      if (data.session_stats.is_last_turn) {
        setPhase('completing');
      }
    },
  });

  const voiceRespondMutation = useMutation({
    mutationFn: async (audioBlob: Blob) => {
      if (!sessionData) throw new Error('No active session');
      return immersiveApi.submitVoiceResponse(sessionData.session_id, audioBlob);
    },
    onSuccess: (data: SubmitResponseResult) => {
      // Same as text response
      const userTurn: ConversationTurn = {
        turn_number: turns.length + 1,
        role: 'user',
        content: data.transcribed_text || '',
        input_type: 'voice',
        grammar_errors: data.user_analysis.grammar_errors,
        vocabulary_feedback: data.user_analysis.vocabulary_feedback,
        score: data.user_analysis.score,
        hint_level_used: 0,
      };
      const newTurns = [...turns, userTurn];

      if (data.npc_response) {
        newTurns.push({
          turn_number: turns.length + 2,
          role: 'npc',
          content: data.npc_response.content,
          audio_url: data.npc_response.audio_url,
          grammar_errors: [],
          vocabulary_feedback: [],
          score: 0,
          hint_level_used: 0,
        });
      }

      setTurns(newTurns);
      setTotalScore((prev) => prev + data.user_analysis.score);
      setTurnCount(data.session_stats.turn_count);

      if (data.session_stats.is_last_turn) {
        setPhase('completing');
      }
    },
  });

  const hintMutation = useMutation({
    mutationFn: async () => {
      if (!sessionData) throw new Error('No active session');
      return immersiveApi.requestHint(sessionData.session_id);
    },
    onSuccess: (data) => {
      setLastHint(data);
      setHintsUsed(3 - data.hints_remaining);
    },
  });

  const completeMutation = useMutation({
    mutationFn: async () => {
      if (!sessionData) throw new Error('No active session');
      return immersiveApi.completeSession(sessionData.session_id);
    },
    onSuccess: (data) => {
      setResult(data);
      setPhase('result');
    },
  });

  const addUserMessage = useCallback((content: string) => {
    setTurns((prev) => {
      const last = prev[prev.length - 1];
      if (last && last.role === 'user' && last.content === '') {
        // Update the placeholder
        return prev.map((t, i) => (i === prev.length - 1 ? { ...t, content } : t));
      }
      return prev;
    });
  }, []);

  return {
    phase,
    sessionData,
    turns,
    totalScore,
    turnCount,
    maxTurns,
    hintsUsed,
    lastHint,
    result,
    startSession: startMutation.mutate,
    isStarting: startMutation.isPending,
    respond: respondMutation.mutate,
    isResponding: respondMutation.isPending,
    respondVoice: voiceRespondMutation.mutate,
    isRespondingVoice: voiceRespondMutation.isPending,
    requestHint: hintMutation.mutate,
    isRequestingHint: hintMutation.isPending,
    completeSession: completeMutation.mutate,
    isCompleting: completeMutation.isPending,
    addUserMessage,
    setPhase,
  };
}

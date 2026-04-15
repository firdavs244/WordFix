/**
 * API functions for the Immersive Language Learning Game.
 */

import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  HintResponse,
  ImmersiveScenario,
  ImmersiveSessionStart,
  SessionCompleteResult,
  SubmitResponseResult,
} from '../types/immersive';

export const immersiveApi = {
  getScenarios: async (params?: { difficulty?: string; location?: string }) => {
    const { data } = await apiClient.get<{ data: ImmersiveScenario[] }>(
      API_ENDPOINTS.IMMERSIVE.SCENARIOS,
      { params },
    );
    return data.data;
  },

  getScenarioDetail: async (id: string) => {
    const { data } = await apiClient.get<{ data: ImmersiveScenario }>(
      API_ENDPOINTS.IMMERSIVE.SCENARIO_DETAIL(id),
    );
    return data.data;
  },

  startSession: async (scenarioId: string, inputMode: string = 'text', npcId?: string) => {
    const { data } = await apiClient.post<{ data: ImmersiveSessionStart }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_START,
      { scenario_id: scenarioId, input_mode: inputMode, ...(npcId && { npc_id: npcId }) },
    );
    return data.data;
  },

  submitResponse: async (sessionId: string, message: string, responseTimeMs?: number) => {
    const { data } = await apiClient.post<{ data: SubmitResponseResult }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_RESPOND(sessionId),
      { message, response_time_ms: responseTimeMs },
    );
    return data.data;
  },

  submitVoiceResponse: async (sessionId: string, audioBlob: Blob, language: string = 'en') => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.webm');
    formData.append('language', language);
    const { data } = await apiClient.post<{ data: SubmitResponseResult }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_RESPOND_VOICE(sessionId),
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return data.data;
  },

  completeSession: async (sessionId: string) => {
    const { data } = await apiClient.post<{ data: SessionCompleteResult }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_COMPLETE(sessionId),
    );
    return data.data;
  },

  requestHint: async (sessionId: string) => {
    const { data } = await apiClient.post<{ data: HintResponse }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_HINT(sessionId),
    );
    return data.data;
  },

  getSessionDetail: async (sessionId: string) => {
    const { data } = await apiClient.get<{ data: any }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_DETAIL(sessionId),
    );
    return data.data;
  },

  getSessionHistory: async (page: number = 1) => {
    const { data } = await apiClient.get<{ data: any[]; meta: { total: number; page: number } }>(
      API_ENDPOINTS.IMMERSIVE.SESSION_HISTORY,
      { params: { page } },
    );
    return data;
  },
};

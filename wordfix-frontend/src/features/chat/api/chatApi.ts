import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  StartChatRequest,
  StartChatResponse,
  SendMessageRequest,
  SendMessageResponse,
  ChatSession,
  ChatSessionDetailResponse,
} from '@/types';

export const chatApi = {
  start: async (data?: StartChatRequest) => {
    const res = await apiClient.post<ApiResponse<StartChatResponse>>(
      API_ENDPOINTS.CHAT.START,
      data || {},
    );
    return res.data;
  },

  sendMessage: async (sessionId: string, data: SendMessageRequest) => {
    const res = await apiClient.post<ApiResponse<SendMessageResponse>>(
      API_ENDPOINTS.CHAT.SEND_MESSAGE(sessionId),
      data,
    );
    return res.data;
  },

  endSession: async (sessionId: string) => {
    const res = await apiClient.post<ApiResponse<ChatSession>>(
      API_ENDPOINTS.CHAT.END(sessionId),
    );
    return res.data;
  },

  getHistory: async (page: number = 1) => {
    const res = await apiClient.get<ApiResponse<ChatSession[]>>(
      `${API_ENDPOINTS.CHAT.HISTORY}?page=${page}`,
    );
    return res.data;
  },

  getSessionDetail: async (sessionId: string) => {
    const res = await apiClient.get<ApiResponse<ChatSessionDetailResponse>>(
      API_ENDPOINTS.CHAT.SESSION_DETAIL(sessionId),
    );
    return res.data;
  },
};

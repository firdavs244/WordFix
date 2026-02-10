import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chatApi } from '../api/chatApi';
import type { StartChatRequest, SendMessageRequest } from '@/types';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const chatKeys = {
  all: ['chat'] as const,
  history: () => [...chatKeys.all, 'history'] as const,
  sessions: () => [...chatKeys.all, 'sessions'] as const,
  session: (id: string) => [...chatKeys.sessions(), id] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useChatHistory(page: number = 1) {
  return useQuery({
    queryKey: [...chatKeys.history(), page],
    queryFn: () => chatApi.getHistory(page),
  });
}

export function useChatSession(sessionId: string) {
  return useQuery({
    queryKey: chatKeys.session(sessionId),
    queryFn: () => chatApi.getSessionDetail(sessionId),
    enabled: !!sessionId,
  });
}

// ─── Mutations ─────────────────────────────────────────────────────────────────

export function useStartChat() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data?: StartChatRequest) => chatApi.start(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.history() });
    },
    onError: () => {
      toast.error('Failed to start chat session.');
    },
  });
}

export function useSendMessage(sessionId: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: SendMessageRequest) => chatApi.sendMessage(sessionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.session(sessionId) });
      queryClient.invalidateQueries({ queryKey: ['daily-challenges'] });
    },
    onError: () => {
      toast.error('Failed to send message.');
    },
  });
}

export function useEndChat() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionId: string) => chatApi.endSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: chatKeys.history() });
      toast.success('Chat session ended.');
    },
    onError: () => {
      toast.error('Failed to end chat session.');
    },
  });
}

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { progressApi, notificationApi } from '../api/progressApi';
import { toast } from 'sonner';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const progressKeys = {
  all: ['progress'] as const,
  progress: () => [...progressKeys.all, 'user'] as const,
  xpHistory: (days?: number) => [...progressKeys.all, 'xp-history', days] as const,
  badges: () => [...progressKeys.all, 'badges'] as const,
  allBadges: () => [...progressKeys.all, 'all-badges'] as const,
};

export const notificationKeys = {
  all: ['notifications'] as const,
  list: (page?: number) => [...notificationKeys.all, 'list', page] as const,
  unreadCount: () => [...notificationKeys.all, 'unread-count'] as const,
};

// ─── Progress Queries ──────────────────────────────────────────────────────────

export function useUserProgress() {
  return useQuery({
    queryKey: progressKeys.progress(),
    queryFn: () => progressApi.getUserProgress(),
  });
}

export function useXPHistory(days = 7) {
  return useQuery({
    queryKey: progressKeys.xpHistory(days),
    queryFn: () => progressApi.getXPHistory(days),
  });
}

export function useUserBadges() {
  return useQuery({
    queryKey: progressKeys.badges(),
    queryFn: () => progressApi.getUserBadges(),
  });
}

export function useAllBadges() {
  return useQuery({
    queryKey: progressKeys.allBadges(),
    queryFn: () => progressApi.getAllBadges(),
  });
}

// ─── Notification Queries ──────────────────────────────────────────────────────

export function useNotifications(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: notificationKeys.list(page),
    queryFn: () => notificationApi.getNotifications(page, pageSize),
  });
}

export function useUnreadNotificationCount() {
  return useQuery({
    queryKey: notificationKeys.unreadCount(),
    queryFn: () => notificationApi.getUnreadCount(),
    refetchInterval: 30000, // Poll every 30s
  });
}

// ─── Notification Mutations ────────────────────────────────────────────────────

export function useMarkNotificationRead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (notificationId: string) => notificationApi.markAsRead(notificationId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationKeys.all });
    },
  });
}

export function useMarkAllNotificationsRead() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => notificationApi.markAllAsRead(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: notificationKeys.all });
      toast.success('All notifications marked as read.');
    },
  });
}

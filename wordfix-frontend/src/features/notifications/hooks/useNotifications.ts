import { useState, useCallback } from 'react';
import {
  useNotifications as useNotificationsQuery,
  useUnreadNotificationCount,
  useMarkNotificationRead,
  useMarkAllNotificationsRead,
} from '@/features/progress/hooks/useProgress';

export function useNotifications() {
  const { data, isLoading } = useNotificationsQuery(1, 20);
  const { data: countData } = useUnreadNotificationCount();
  const markReadMutation = useMarkNotificationRead();
  const markAllReadMutation = useMarkAllNotificationsRead();

  const [isPanelOpen, setIsPanelOpen] = useState(false);

  const togglePanel = useCallback(() => setIsPanelOpen((p) => !p), []);
  const closePanel = useCallback(() => setIsPanelOpen(false), []);

  return {
    notifications: data?.data?.notifications ?? [],
    unreadCount: countData?.data?.count ?? 0,
    markRead: markReadMutation.mutate,
    markAllRead: markAllReadMutation.mutate,
    isLoading,
    isPanelOpen,
    togglePanel,
    closePanel,
  };
}

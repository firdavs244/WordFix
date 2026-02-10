import type { NotificationType } from './core';

// ─── Notification Types ────────────────────────────────────────────────────────

export interface NotificationData {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  is_read: boolean;
  data: Record<string, unknown>;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: NotificationData[];
  unread_count: number;
}

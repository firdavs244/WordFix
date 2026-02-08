import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  UserProgressData,
  XPHistoryEntry,
  UserBadgesResponse,
  BadgeData,
  NotificationListResponse,
} from '@/types';

// ─── Progress API ──────────────────────────────────────────────────────────────

export const progressApi = {
  getUserProgress: () =>
    apiClient
      .get<ApiResponse<UserProgressData>>(API_ENDPOINTS.PROGRESS.USER_PROGRESS)
      .then((r) => r.data),

  getXPHistory: (days = 7) =>
    apiClient
      .get<ApiResponse<XPHistoryEntry[]>>(API_ENDPOINTS.PROGRESS.XP_HISTORY, {
        params: { days },
      })
      .then((r) => r.data),

  getUserBadges: () =>
    apiClient
      .get<ApiResponse<UserBadgesResponse>>(API_ENDPOINTS.PROGRESS.USER_BADGES)
      .then((r) => r.data),

  getAllBadges: () =>
    apiClient
      .get<ApiResponse<BadgeData[]>>(API_ENDPOINTS.PROGRESS.ALL_BADGES)
      .then((r) => r.data),
};

// ─── Notification API ──────────────────────────────────────────────────────────

export const notificationApi = {
  getNotifications: (page = 1, pageSize = 20) =>
    apiClient
      .get<ApiResponse<NotificationListResponse>>(API_ENDPOINTS.NOTIFICATIONS.LIST, {
        params: { page, page_size: pageSize },
      })
      .then((r) => r.data),

  markAsRead: (notificationId: string) =>
    apiClient
      .post<ApiResponse<unknown>>(API_ENDPOINTS.NOTIFICATIONS.MARK_READ, {
        notification_id: notificationId,
      })
      .then((r) => r.data),

  markAllAsRead: () =>
    apiClient
      .post<ApiResponse<{ marked_count: number }>>(API_ENDPOINTS.NOTIFICATIONS.MARK_READ, {
        all: true,
      })
      .then((r) => r.data),

  getUnreadCount: () =>
    apiClient
      .get<ApiResponse<{ count: number }>>(API_ENDPOINTS.NOTIFICATIONS.UNREAD_COUNT)
      .then((r) => r.data),
};

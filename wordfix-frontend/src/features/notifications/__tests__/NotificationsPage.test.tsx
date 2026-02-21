import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { NotificationsPage } from '../NotificationsPage';

vi.mock('../hooks/useNotifications', () => ({
  useNotifications: () => ({
    notifications: [
      {
        id: 'n1',
        type: 'badge_earned',
        title: 'New Badge!',
        message: 'You earned the First Word badge',
        is_read: false,
        data: {},
        created_at: new Date().toISOString(),
      },
      {
        id: 'n2',
        type: 'streak_warning',
        title: 'Streak Warning',
        message: 'Practice today to keep your streak',
        is_read: true,
        data: {},
        created_at: new Date().toISOString(),
      },
    ],
    unreadCount: 1,
    isLoading: false,
    markRead: vi.fn(),
    markAllRead: vi.fn(),
    isPanelOpen: false,
    togglePanel: vi.fn(),
    closePanel: vi.fn(),
  }),
}));

describe('NotificationsPage', () => {
  it('renders page header', () => {
    render(<NotificationsPage />);
    expect(screen.getByText('Notifications')).toBeInTheDocument();
  });

  it('renders notification items', () => {
    render(<NotificationsPage />);
    expect(screen.getByText('New Badge!')).toBeInTheDocument();
    expect(screen.getByText('Streak Warning')).toBeInTheDocument();
  });

  it('shows mark all read button when there are unread', () => {
    render(<NotificationsPage />);
    expect(screen.getByText('Mark all read')).toBeInTheDocument();
  });
});

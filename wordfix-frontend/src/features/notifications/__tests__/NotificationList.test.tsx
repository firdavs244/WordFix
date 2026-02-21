import { describe, it, expect, vi } from 'vitest';
import { render, screen, createMockNotification } from '@/test/utils';
import { NotificationList } from '../components/NotificationList';

describe('NotificationList', () => {
  it('shows loading skeletons when loading', () => {
    const { container } = render(
      <NotificationList notifications={[]} isLoading={true} onMarkRead={vi.fn()} />,
    );
    const skeletons = container.querySelectorAll('[class*="animate-pulse"], [data-slot="skeleton"]');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('shows empty state when no notifications', () => {
    render(
      <NotificationList notifications={[]} isLoading={false} onMarkRead={vi.fn()} />,
    );
    expect(screen.getByText('No notifications yet')).toBeInTheDocument();
  });

  it('renders notification items', () => {
    const notifications = [
      createMockNotification({ id: '1', title: 'First' }),
      createMockNotification({ id: '2', title: 'Second' }),
    ];
    render(
      <NotificationList
        notifications={notifications}
        isLoading={false}
        onMarkRead={vi.fn()}
      />,
    );
    expect(screen.getByText('First')).toBeInTheDocument();
    expect(screen.getByText('Second')).toBeInTheDocument();
  });
});

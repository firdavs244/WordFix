import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent, createMockNotification } from '@/test/utils';
import { NotificationPanel } from '../components/NotificationPanel';

describe('NotificationPanel', () => {
  const baseProps = {
    isOpen: true,
    notifications: [
      createMockNotification({ id: '1', title: 'Badge earned' }),
    ],
    unreadCount: 1,
    isLoading: false,
    onClose: vi.fn(),
    onMarkRead: vi.fn(),
    onMarkAllRead: vi.fn(),
  };

  it('renders panel header when open', () => {
    render(<NotificationPanel {...baseProps} />);
    expect(screen.getByText('Notifications')).toBeInTheDocument();
  });

  it('shows mark all read button when unread > 0', () => {
    render(<NotificationPanel {...baseProps} />);
    expect(screen.getByText('Mark all read')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(<NotificationPanel {...baseProps} isOpen={false} />);
    expect(screen.queryByText('Notifications')).not.toBeInTheDocument();
  });

  it('calls onClose when backdrop is clicked', async () => {
    const onClose = vi.fn();
    const user = userEvent.setup();
    render(
      <NotificationPanel {...baseProps} onClose={onClose} />,
    );
    const backdrop = document.querySelector('[aria-hidden="true"]');
    if (backdrop) await user.click(backdrop);
    expect(onClose).toHaveBeenCalled();
  });
});

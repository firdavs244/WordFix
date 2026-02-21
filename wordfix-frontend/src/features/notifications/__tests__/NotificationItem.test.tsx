import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent, createMockNotification } from '@/test/utils';
import { NotificationItem } from '../components/NotificationItem';

describe('NotificationItem', () => {
  it('renders notification title and message', () => {
    const n = createMockNotification({ title: 'Level Up!', message: 'B1 reached' });
    render(<NotificationItem notification={n} onMarkRead={vi.fn()} />);
    expect(screen.getByText('Level Up!')).toBeInTheDocument();
    expect(screen.getByText('B1 reached')).toBeInTheDocument();
  });

  it('shows unread dot for unread notifications', () => {
    const n = createMockNotification({ is_read: false, title: 'Test' });
    render(<NotificationItem notification={n} onMarkRead={vi.fn()} />);
    expect(screen.getByLabelText(/Mark "Test" as read/)).toBeInTheDocument();
  });

  it('hides unread dot for read notifications', () => {
    const n = createMockNotification({ is_read: true, title: 'Test' });
    render(<NotificationItem notification={n} onMarkRead={vi.fn()} />);
    expect(screen.queryByLabelText(/Mark .* as read/)).not.toBeInTheDocument();
  });

  it('calls onMarkRead when dot is clicked', async () => {
    const onMarkRead = vi.fn();
    const n = createMockNotification({ id: 'n99', is_read: false, title: 'Click me' });
    const user = userEvent.setup();
    render(
      <NotificationItem notification={n} onMarkRead={onMarkRead} />,
    );
    await user.click(screen.getByLabelText(/Mark "Click me" as read/));
    expect(onMarkRead).toHaveBeenCalledWith('n99');
  });
});

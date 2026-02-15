import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent, waitFor } from '@/test/utils';
import SessionTypeCard from '../SessionTypeCard';
import { Brain } from 'lucide-react';

// Mock MouseTiltCard
vi.mock('@/features/dashboard/components/MouseTiltCard', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useNavigate: () => mockNavigate };
});

describe('SessionTypeCard', () => {
  const props = {
    type: 'review' as const,
    title: 'Review',
    description: 'Review due words',
    icon: Brain,
    gradient: 'from-primary/5 to-primary/10',
    iconGradient: 'from-primary to-primary/80',
    count: 12,
  };

  beforeEach(() => mockNavigate.mockClear());

  it('renders title and description', () => {
    render(<SessionTypeCard {...props} />);
    expect(screen.getByText('Review')).toBeInTheDocument();
    expect(screen.getByText('Review due words')).toBeInTheDocument();
  });

  it('renders word count badge when count provided', () => {
    render(<SessionTypeCard {...props} />);
    expect(screen.getByText('12 words')).toBeInTheDocument();
  });

  it('does not render word count badge when count is undefined', () => {
    render(<SessionTypeCard {...props} count={undefined} />);
    expect(screen.queryByText(/words/)).not.toBeInTheDocument();
  });

  it('has disabled styles when disabled', () => {
    render(<SessionTypeCard {...props} disabled />);
    const el = screen.getByRole('button');
    expect(el).toHaveAttribute('aria-disabled', 'true');
    expect(el.className).toContain('opacity-50');
  });

  it('starts session and navigates on click', async () => {
    const user = userEvent.setup();
    render(<SessionTypeCard {...props} />);
    await user.click(screen.getByRole('button'));
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith(
        expect.stringContaining('/review/session/'),
        expect.objectContaining({ state: { sessionType: 'review' } }),
      );
    });
  });

  it('does not navigate when disabled', async () => {
    const user = userEvent.setup();
    render(<SessionTypeCard {...props} disabled />);
    await user.click(screen.getByRole('button'));
    expect(mockNavigate).not.toHaveBeenCalled();
  });
});

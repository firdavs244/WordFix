import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { StreakWidget } from '../StreakWidget';

vi.mock('../../hooks/useReview', () => ({
  useStreak: () => ({
    data: {
      data: {
        current_streak: 7,
        longest_streak: 14,
        total_review_days: 30,
        streak_frozen_until: null,
      },
    },
    isLoading: false,
  }),
}));

describe('StreakWidget', () => {
  it('renders compact mode with streak count', () => {
    render(<StreakWidget compact />);
    expect(screen.getByText('7')).toBeInTheDocument();
  });

  it('renders full mode with current streak', () => {
    render(<StreakWidget />);
    expect(screen.getByText(/7/)).toBeInTheDocument();
    expect(screen.getByText('Current Streak')).toBeInTheDocument();
  });

  it('shows best streak', () => {
    render(<StreakWidget />);
    expect(screen.getByText(/Best: 14/)).toBeInTheDocument();
  });
});

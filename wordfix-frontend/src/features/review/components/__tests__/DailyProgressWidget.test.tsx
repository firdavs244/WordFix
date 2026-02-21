import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { DailyProgressWidget } from '../DailyProgressWidget';

vi.mock('../../hooks/useReview', () => ({
  useDailyProgress: () => ({
    data: {
      data: {
        id: 'dp1',
        words_reviewed: 8,
        words_added: 3,
        words_mastered: 2,
        correct_answers: 15,
        incorrect_answers: 3,
        total_time_seconds: 720,
        goal_completed: false,
        xp_earned: 45,
        date: new Date().toISOString().split('T')[0],
      },
    },
    isLoading: false,
  }),
}));

vi.mock('@/stores/useAuthStore', () => ({
  useAuthStore: (selector: (s: Record<string, unknown>) => unknown) =>
    selector({ user: { daily_goal: 10 }, isAuthenticated: true }),
}));

describe('DailyProgressWidget', () => {
  it('renders today\'s progress heading', () => {
    render(<DailyProgressWidget />);
    expect(screen.getByText("Today's Progress")).toBeInTheDocument();
  });

  it('shows words reviewed / daily goal', () => {
    render(<DailyProgressWidget />);
    expect(screen.getByText('8/10 words')).toBeInTheDocument();
  });

  it('shows XP earned', () => {
    render(<DailyProgressWidget />);
    expect(screen.getByText('+45 XP')).toBeInTheDocument();
  });

  it('shows mastered count', () => {
    render(<DailyProgressWidget />);
    expect(screen.getByText('2')).toBeInTheDocument();
  });
});

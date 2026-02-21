import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import BadgesGrid from '../BadgesGrid';

vi.mock('../../hooks/useBadges', () => ({
  useBadges: () => ({
    badges: [
      { id: 'b1', name: 'First Word', category: 'words', rarity: 'common', is_earned: true, earned_at: '2025-01-01', description: 'Add first word', xp_reward: 10, code: 'first_word', icon: '' },
      { id: 'b2', name: 'Week Warrior', category: 'streak', rarity: 'rare', is_earned: false, earned_at: null, description: '7 day streak', xp_reward: 50, code: 'streak_7', icon: '' },
      { id: 'b3', name: 'Test Ace', category: 'test', rarity: 'epic', is_earned: false, earned_at: null, description: 'Perfect test', xp_reward: 75, code: 'test_ace', icon: '' },
    ],
    isLoading: false,
    earnedCount: 1,
    totalCount: 3,
  }),
}));

describe('BadgesGrid', () => {
  it('renders correct number of badge cards', () => {
    render(<BadgesGrid category="all" />);
    expect(screen.getByText('First Word')).toBeInTheDocument();
    expect(screen.getByText('Week Warrior')).toBeInTheDocument();
    expect(screen.getByText('Test Ace')).toBeInTheDocument();
  });

  it('filters by category correctly', () => {
    render(<BadgesGrid category="words" />);
    expect(screen.getByText('First Word')).toBeInTheDocument();
    expect(screen.queryByText('Week Warrior')).not.toBeInTheDocument();
  });

  it('shows empty state when filter yields no results', () => {
    render(<BadgesGrid category="game" />);
    expect(screen.getByText('No badges in this category')).toBeInTheDocument();
  });
});

import { describe, it, expect } from 'vitest';
import { render, screen, createMockBadge } from '@/test/utils';
import BadgeCard from '../BadgeCard';

describe('BadgeCard', () => {
  it('renders earned badge with trophy icon', () => {
    const badge = createMockBadge({ is_earned: true, earned_at: '2025-01-01' });
    render(<BadgeCard badge={badge} />);
    expect(screen.getByLabelText('trophy')).toBeInTheDocument();
  });

  it('renders locked badge with lock icon', () => {
    const badge = createMockBadge({ is_earned: false, earned_at: null });
    render(<BadgeCard badge={badge} />);
    expect(screen.getByLabelText('locked')).toBeInTheDocument();
  });

  it('shows badge name and description', () => {
    const badge = createMockBadge({ name: 'Word Master', description: 'Master 10 words' });
    render(<BadgeCard badge={badge} />);
    expect(screen.getByText('Word Master')).toBeInTheDocument();
    expect(screen.getByText('Master 10 words')).toBeInTheDocument();
  });

  it('shows XP value for earned badge', () => {
    const badge = createMockBadge({ is_earned: true, earned_at: '2025-01-01', xp_reward: 50 });
    render(<BadgeCard badge={badge} />);
    expect(screen.getByText('+50 XP')).toBeInTheDocument();
  });

  it('applies reduced opacity for locked badge', () => {
    const badge = createMockBadge({ is_earned: false, earned_at: null });
    const { container } = render(<BadgeCard badge={badge} />);
    expect(container.querySelector('.opacity-50')).toBeInTheDocument();
  });

  it('shows rarity label text', () => {
    const badge = createMockBadge({ is_earned: true, earned_at: '2025-01-01', rarity: 'epic' });
    render(<BadgeCard badge={badge} />);
    expect(screen.getByText('epic')).toBeInTheDocument();
  });

  it('renders common styling for common rarity', () => {
    const badge = createMockBadge({ is_earned: true, earned_at: '2025-01-01', rarity: 'common' });
    const { container } = render(<BadgeCard badge={badge} />);
    expect(container.querySelector('.border-border\\/50')).toBeInTheDocument();
  });

  it('renders blue styling for rare rarity', () => {
    const badge = createMockBadge({ is_earned: true, earned_at: '2025-01-01', rarity: 'rare' });
    const { container } = render(<BadgeCard badge={badge} />);
    expect(container.querySelector('.border-blue-500\\/30')).toBeInTheDocument();
  });
});

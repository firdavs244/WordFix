import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { LearningRecommendations } from '../components/LearningRecommendations';

const mockRecs = [
  {
    id: 'r1',
    word: 'ephemeral',
    translation: 'vaqtinchalik',
    reason: 'High frequency word you should know',
    reason_type: 'high_frequency' as const,
    priority: 1,
    is_accepted: false,
    ai_confidence: 0.9,
  },
];

describe('LearningRecommendations', () => {
  it('shows empty state when no recommendations', () => {
    render(
      <LearningRecommendations
        recommendations={[]}
        isLoading={false}
        onAccept={vi.fn()}
        isPending={false}
      />,
    );
    expect(screen.getByText('No recommendations')).toBeInTheDocument();
  });

  it('renders recommendation items', () => {
    render(
      <LearningRecommendations
        recommendations={mockRecs}
        isLoading={false}
        onAccept={vi.fn()}
        isPending={false}
      />,
    );
    expect(screen.getByText('ephemeral')).toBeInTheDocument();
  });
});

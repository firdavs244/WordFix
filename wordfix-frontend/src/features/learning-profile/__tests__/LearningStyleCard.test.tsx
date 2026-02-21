import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import { LearningStyleCard } from '../components/LearningStyleCard';
import { createMockLearningProfile } from '@/test/utils';

describe('LearningStyleCard', () => {
  it('shows loading skeletons when loading', () => {
    const { container } = render(
      <LearningStyleCard profile={null} isLoading={true} hasAnalyzed={false} />,
    );
    const skeletons = container.querySelectorAll('.animate-pulse');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  it('shows prompt when not analyzed', () => {
    render(
      <LearningStyleCard profile={null} isLoading={false} hasAnalyzed={false} />,
    );
    expect(screen.getByText(/Run an analysis/)).toBeInTheDocument();
  });

  it('renders style when analyzed', () => {
    const profile = createMockLearningProfile();
    render(
      <LearningStyleCard profile={profile} isLoading={false} hasAnalyzed={true} />,
    );
    expect(screen.getAllByText('Visual Learner').length).toBeGreaterThan(0);
  });
});

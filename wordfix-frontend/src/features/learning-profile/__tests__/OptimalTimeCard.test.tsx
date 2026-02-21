import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import { OptimalTimeCard } from '../components/OptimalTimeCard';
import { createMockLearningProfile } from '@/test/utils';

describe('OptimalTimeCard', () => {
  it('shows prompt when not analyzed', () => {
    render(
      <OptimalTimeCard profile={null} isLoading={false} hasAnalyzed={false} />,
    );
    expect(screen.getByText(/Run an analysis/)).toBeInTheDocument();
  });

  it('renders optimal hours when analyzed', () => {
    const profile = createMockLearningProfile();
    render(
      <OptimalTimeCard profile={profile} isLoading={false} hasAnalyzed={true} />,
    );
    expect(screen.getByText(/09:00/)).toBeInTheDocument();
  });

  it('renders day indicators', () => {
    const profile = createMockLearningProfile();
    render(
      <OptimalTimeCard profile={profile} isLoading={false} hasAnalyzed={true} />,
    );
    expect(screen.getByText('Du')).toBeInTheDocument();
  });
});

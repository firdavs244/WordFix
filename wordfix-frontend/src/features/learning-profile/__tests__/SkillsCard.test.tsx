import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import { SkillsCard } from '../components/SkillsCard';
import { createMockLearningProfile } from '@/test/utils';

describe('SkillsCard', () => {
  it('shows prompt when not analyzed', () => {
    render(
      <SkillsCard profile={null} isLoading={false} hasAnalyzed={false} />,
    );
    expect(screen.getByText(/Run an analysis/)).toBeInTheDocument();
  });

  it('renders skill labels when analyzed', () => {
    const profile = createMockLearningProfile();
    render(
      <SkillsCard profile={profile} isLoading={false} hasAnalyzed={true} />,
    );
    expect(screen.getByText('Reading')).toBeInTheDocument();
    expect(screen.getByText('Vocabulary')).toBeInTheDocument();
  });

  it('shows strong badge for strongest skills', () => {
    const profile = createMockLearningProfile();
    render(
      <SkillsCard profile={profile} isLoading={false} hasAnalyzed={true} />,
    );
    expect(screen.getByText('Strong')).toBeInTheDocument();
  });
});

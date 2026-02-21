import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { LevelProgress } from '../LevelProgress';

vi.mock('../../hooks/useProgress', () => ({
  useUserProgress: () => ({
    data: {
      data: {
        level: 5,
        total_xp: 1250,
        xp_progress: 50,
        xp_needed: 200,
        progress_pct: 25,
      },
    },
    isLoading: false,
  }),
}));

describe('LevelProgress', () => {
  it('renders compact mode with level and XP', () => {
    render(<LevelProgress compact />);
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('1250 XP')).toBeInTheDocument();
  });

  it('renders full mode with progress bar', () => {
    render(<LevelProgress />);
    expect(screen.getByText('Level 5')).toBeInTheDocument();
    expect(screen.getByText('1250 XP')).toBeInTheDocument();
  });

  it('shows next level target', () => {
    render(<LevelProgress />);
    expect(screen.getByText('Level 6')).toBeInTheDocument();
  });
});

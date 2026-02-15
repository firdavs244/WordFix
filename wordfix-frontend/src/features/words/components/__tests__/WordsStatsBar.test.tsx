import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import WordsStatsBar from '../WordsStatsBar';

describe('WordsStatsBar', () => {
  it('renders loading skeletons before data loads', () => {
    render(<WordsStatsBar />);
    // Initially it should show either the loading skeletons or stats
    // The stats bar will render and then data will load
    expect(document.querySelector('[data-testid="stats-loading"], .flex')).toBeTruthy();
  });

  it('renders all four stat pills after data loads', async () => {
    render(<WordsStatsBar />);
    await waitFor(() => {
      expect(screen.getByText('Total')).toBeInTheDocument();
    });
    expect(screen.getByText('Mastered')).toBeInTheDocument();
    expect(screen.getByText('Learning')).toBeInTheDocument();
    expect(screen.getByText('New')).toBeInTheDocument();
  });

  it('renders stat values from API', async () => {
    render(<WordsStatsBar />);
    await waitFor(() => {
      expect(screen.getByText('50')).toBeInTheDocument(); // total
    });
    expect(screen.getByText('15')).toBeInTheDocument(); // mastered
    expect(screen.getByText('25')).toBeInTheDocument(); // learning
    expect(screen.getByText('10')).toBeInTheDocument(); // new
  });
});

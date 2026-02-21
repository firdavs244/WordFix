import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import WeeklyChart from '../../components/WeeklyChart';
import type { DailyStatsEntry } from '@/types';

const data: DailyStatsEntry[] = [
  { date: '2025-01-13', words_reviewed: 8, words_added: 2, correct_answers: 6, incorrect_answers: 2, xp_earned: 40, total_time_seconds: 1200 },
  { date: '2025-01-14', words_reviewed: 12, words_added: 3, correct_answers: 10, incorrect_answers: 2, xp_earned: 60, total_time_seconds: 1800 },
];

describe('WeeklyChart', () => {
  it('renders heading', () => {
    render(<WeeklyChart data={data} />);
    expect(screen.getByText('This Week')).toBeInTheDocument();
  });

  it('shows total count', () => {
    render(<WeeklyChart data={data} />);
    expect(screen.getByText('20')).toBeInTheDocument();
  });

  it('renders bars for each day', () => {
    render(<WeeklyChart data={data} />);
    expect(screen.getByText('Mon')).toBeInTheDocument();
    expect(screen.getByText('Tue')).toBeInTheDocument();
  });

  it('shows empty state when no data', () => {
    render(<WeeklyChart data={[]} />);
    expect(screen.getByText(/no data/i)).toBeInTheDocument();
  });
});

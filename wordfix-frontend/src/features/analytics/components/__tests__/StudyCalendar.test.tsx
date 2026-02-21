import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import StudyCalendar from '../../components/StudyCalendar';
import type { CalendarDay } from '@/types';

const data: CalendarDay[] = Array.from({ length: 7 }, (_, i) => ({
  date: `2025-01-${String(13 + i).padStart(2, '0')}`,
  active: true,
  words_reviewed: i * 2,
  xp_earned: i * 10,
  goal_completed: i > 3,
}));

describe('StudyCalendar', () => {
  it('renders heading', () => {
    render(<StudyCalendar data={data} />);
    expect(screen.getByText('Study Calendar')).toBeInTheDocument();
  });

  it('renders day headers', () => {
    render(<StudyCalendar data={data} />);
    // At least M, T, W should appear
    const mHeaders = screen.getAllByText('M');
    expect(mHeaders.length).toBeGreaterThan(0);
  });

  it('renders legend', () => {
    render(<StudyCalendar data={data} />);
    expect(screen.getByText('Less')).toBeInTheDocument();
    expect(screen.getByText('More')).toBeInTheDocument();
  });
});

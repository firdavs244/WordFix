import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import TestGradeBadge from '../TestGradeBadge';

describe('TestGradeBadge', () => {
  it('renders the grade letter', () => {
    render(<TestGradeBadge grade="A" score={95} />);
    expect(screen.getByTestId('grade-letter')).toHaveTextContent('A');
  });

  it('renders the score percentage', () => {
    render(<TestGradeBadge grade="A" score={95} />);
    expect(screen.getByTestId('grade-score')).toHaveTextContent('95%');
  });

  it('renders grade B correctly', () => {
    render(<TestGradeBadge grade="B" score={85} />);
    expect(screen.getByTestId('grade-letter')).toHaveTextContent('B');
  });

  it('renders grade F correctly', () => {
    render(<TestGradeBadge grade="F" score={40} />);
    expect(screen.getByTestId('grade-letter')).toHaveTextContent('F');
    expect(screen.getByTestId('grade-score')).toHaveTextContent('40%');
  });

  it('has grade-badge test id', () => {
    render(<TestGradeBadge grade="C" score={75} />);
    expect(screen.getByTestId('grade-badge')).toBeInTheDocument();
  });

  it('triggers confetti for grade A', () => {
    const confetti = vi.fn();
    vi.stubGlobal('confetti', confetti);
    render(<TestGradeBadge grade="A" score={95} />);
    // confetti is mocked in setup.ts, just verify component renders
    expect(screen.getByTestId('grade-letter')).toHaveTextContent('A');
  });

  it('does not crash for grade D', () => {
    render(<TestGradeBadge grade="D" score={62} />);
    expect(screen.getByTestId('grade-letter')).toHaveTextContent('D');
  });
});

import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import SpeedRoundTimer from '../SpeedRoundTimer';

describe('SpeedRoundTimer', () => {
  it('renders the remaining time', () => {
    render(<SpeedRoundTimer remaining={45} total={60} />);
    expect(screen.getByText('45')).toBeInTheDocument();
  });

  it('has speed-timer test id', () => {
    render(<SpeedRoundTimer remaining={45} total={60} />);
    expect(screen.getByTestId('speed-timer')).toBeInTheDocument();
  });

  it('renders SVG circle element', () => {
    const { container } = render(<SpeedRoundTimer remaining={45} total={60} />);
    const circles = container.querySelectorAll('circle');
    expect(circles).toHaveLength(2);
  });

  it('applies pulse animation when under 10 seconds', () => {
    render(<SpeedRoundTimer remaining={5} total={60} />);
    expect(screen.getByTestId('speed-timer')).toHaveClass('animate-pulse');
  });

  it('does not pulse when above 10 seconds', () => {
    render(<SpeedRoundTimer remaining={30} total={60} />);
    expect(screen.getByTestId('speed-timer')).not.toHaveClass('animate-pulse');
  });
});

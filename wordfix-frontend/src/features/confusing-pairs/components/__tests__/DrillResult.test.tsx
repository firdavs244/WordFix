import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import { DrillResult } from '../../components/DrillResult';

describe('DrillResult', () => {
  const onResolve = vi.fn();
  const onRetry = vi.fn();
  const onClose = vi.fn();

  it('renders score', () => {
    render(<DrillResult correct={2} total={3} scorePct={67} onResolve={onResolve} onRetry={onRetry} onClose={onClose} />);
    expect(screen.getByText(/2\/3/)).toBeInTheDocument();
    expect(screen.getByText(/67%/)).toBeInTheDocument();
  });

  it('shows drill complete heading', () => {
    render(<DrillResult correct={3} total={3} scorePct={100} onResolve={onResolve} onRetry={onRetry} onClose={onClose} />);
    expect(screen.getByText(/drill complete/i)).toBeInTheDocument();
  });

  it('shows resolve button for high scores', () => {
    render(<DrillResult correct={3} total={3} scorePct={100} onResolve={onResolve} onRetry={onRetry} onClose={onClose} />);
    expect(screen.getByText(/mark as resolved/i)).toBeInTheDocument();
  });

  it('hides resolve button for low scores', () => {
    render(<DrillResult correct={1} total={3} scorePct={33} onResolve={onResolve} onRetry={onRetry} onClose={onClose} />);
    expect(screen.queryByText(/mark as resolved/i)).not.toBeInTheDocument();
  });

  it('calls onRetry when retry button clicked', async () => {
    const user = userEvent.setup();
    render(<DrillResult correct={2} total={3} scorePct={67} onResolve={onResolve} onRetry={onRetry} onClose={onClose} />);
    await user.click(screen.getByText(/practice again/i));
    expect(onRetry).toHaveBeenCalled();
  });
});

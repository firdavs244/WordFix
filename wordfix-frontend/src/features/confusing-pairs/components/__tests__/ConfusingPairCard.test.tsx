import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import { ConfusingPairCard } from '../../components/ConfusingPairCard';
import { createMockConfusingPair } from '@/test/utils';

describe('ConfusingPairCard', () => {
  const onDrill = vi.fn();
  const onResolve = vi.fn();

  it('renders both words', () => {
    const pair = createMockConfusingPair();
    render(<ConfusingPairCard pair={pair} onDrill={onDrill} onResolve={onResolve} />);
    expect(screen.getByText('affect')).toBeInTheDocument();
    expect(screen.getByText('effect')).toBeInTheDocument();
  });

  it('shows confusion count', () => {
    const pair = createMockConfusingPair({ confusion_count: 7 });
    render(<ConfusingPairCard pair={pair} onDrill={onDrill} onResolve={onResolve} />);
    expect(screen.getByText(/confused 7 times/i)).toBeInTheDocument();
  });

  it('shows practice drill button for unresolved pairs', () => {
    const pair = createMockConfusingPair({ is_resolved: false });
    render(<ConfusingPairCard pair={pair} onDrill={onDrill} onResolve={onResolve} />);
    expect(screen.getByText(/practice drill/i)).toBeInTheDocument();
  });

  it('hides action buttons for resolved pairs', () => {
    const pair = createMockConfusingPair({ is_resolved: true });
    render(<ConfusingPairCard pair={pair} onDrill={onDrill} onResolve={onResolve} />);
    expect(screen.queryByText(/practice drill/i)).not.toBeInTheDocument();
  });

  it('calls onDrill when drill button is clicked', async () => {
    const user = userEvent.setup();
    const pair = createMockConfusingPair({ id: 'cp-5' });
    render(<ConfusingPairCard pair={pair} onDrill={onDrill} onResolve={onResolve} />);
    await user.click(screen.getByText(/practice drill/i));
    expect(onDrill).toHaveBeenCalledWith('cp-5');
  });
});

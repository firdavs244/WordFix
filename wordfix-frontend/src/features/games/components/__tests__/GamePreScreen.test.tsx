import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import { Zap } from 'lucide-react';
import GamePreScreen from '../GamePreScreen';

describe('GamePreScreen', () => {
  const onStart = vi.fn();
  const rules = ['Rule 1', 'Rule 2', 'Rule 3'];

  beforeEach(() => onStart.mockClear());

  it('renders the game title', () => {
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} />);
    expect(screen.getByText('Speed Round')).toBeInTheDocument();
  });

  it('renders all rules', () => {
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} />);
    expect(screen.getByText('Rule 1')).toBeInTheDocument();
    expect(screen.getByText('Rule 2')).toBeInTheDocument();
    expect(screen.getByText('Rule 3')).toBeInTheDocument();
  });

  it('renders numbered rule indicators', () => {
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} />);
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('renders Start Game button', () => {
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} />);
    expect(screen.getByText('Start Game')).toBeInTheDocument();
  });

  it('calls onStart when button clicked', async () => {
    const user = userEvent.setup();
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} />);
    await user.click(screen.getByText('Start Game'));
    expect(onStart).toHaveBeenCalledTimes(1);
  });

  it('shows loading spinner when isLoading', () => {
    render(<GamePreScreen title="Speed Round" icon={Zap} rules={rules} onStart={onStart} isLoading />);
    expect(screen.queryByText('Start Game')).not.toBeInTheDocument();
  });
});

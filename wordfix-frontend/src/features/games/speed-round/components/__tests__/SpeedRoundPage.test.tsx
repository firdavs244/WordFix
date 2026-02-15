import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import SpeedRoundPage from '../../SpeedRoundPage';

vi.mock('../../components/SpeedRoundCountdown', () => ({ default: ({ onComplete }: { onComplete: () => void }) => <div data-testid="countdown"><button onClick={onComplete}>Go</button></div> }));
vi.mock('../../components/SpeedRoundTimer', () => ({ default: ({ remaining }: { remaining: number }) => <div data-testid="timer">{remaining}s</div> }));
vi.mock('../../components/SpeedRoundWord', () => ({ default: ({ word }: { word: string }) => <div data-testid="word">{word}</div> }));
vi.mock('../../components/SpeedRoundOptions', () => ({ default: () => <div data-testid="options">Options</div> }));
vi.mock('../../../components/GameComboIndicator', () => ({ default: () => <div data-testid="combo" /> }));
vi.mock('../../../components/GamePreScreen', () => ({
  default: ({ title, onStart }: { title: string; onStart: () => void }) => (
    <div data-testid="pre-screen">
      <span>{title}</span>
      <button onClick={onStart}>Start Game</button>
    </div>
  ),
}));

describe('SpeedRoundPage', () => {
  it('renders pre-screen initially', () => {
    render(<SpeedRoundPage />);
    expect(screen.getByTestId('pre-screen')).toBeInTheDocument();
  });

  it('renders Speed Round title on pre-screen', () => {
    render(<SpeedRoundPage />);
    expect(screen.getByText('Speed Round')).toBeInTheDocument();
  });

  it('renders Start Game button', () => {
    render(<SpeedRoundPage />);
    expect(screen.getByText('Start Game')).toBeInTheDocument();
  });

  it('renders the pre-screen with correct title', () => {
    render(<SpeedRoundPage />);
    expect(screen.getByText('Speed Round')).toBeInTheDocument();
  });
});

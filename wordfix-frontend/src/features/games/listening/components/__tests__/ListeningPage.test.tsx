import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import ListeningPage from '../../ListeningPage';

vi.mock('../../components/AudioPlayer', () => ({ default: () => <div data-testid="audio-player">Player</div> }));
vi.mock('../../components/AttemptIndicator', () => ({ default: () => <div data-testid="attempts">Attempts</div> }));
vi.mock('../../components/ListeningInput', () => ({ default: () => <div data-testid="listening-input">Input</div> }));
vi.mock('../../components/ListeningFeedback', () => ({ default: () => <div data-testid="listening-feedback">Feedback</div> }));
vi.mock('../../components/ListeningComplete', () => ({ default: () => <div data-testid="listening-complete">Complete</div> }));
vi.mock('../../../components/GamePreScreen', () => ({
  default: ({ title, onStart }: { title: string; onStart: () => void }) => (
    <div data-testid="pre-screen">
      <span>{title}</span>
      <button onClick={onStart}>Start Game</button>
    </div>
  ),
}));

describe('ListeningPage', () => {
  it('renders pre-screen initially', () => {
    render(<ListeningPage />);
    expect(screen.getByTestId('pre-screen')).toBeInTheDocument();
  });

  it('renders Listening Challenge title on pre-screen', () => {
    render(<ListeningPage />);
    expect(screen.getByText('Listening Challenge')).toBeInTheDocument();
  });

  it('renders Start Game button', () => {
    render(<ListeningPage />);
    expect(screen.getByText('Start Game')).toBeInTheDocument();
  });

  it('renders without crashing', () => {
    const { container } = render(<ListeningPage />);
    expect(container.firstChild).toBeDefined();
  });
});

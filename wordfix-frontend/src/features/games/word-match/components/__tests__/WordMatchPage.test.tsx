import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import WordMatchPage from '../../WordMatchPage';

vi.mock('../../components/WordMatchBoard', () => ({ default: () => <div data-testid="match-board">Board</div> }));
vi.mock('../../../components/GameComboIndicator', () => ({ default: () => <div data-testid="combo" /> }));
vi.mock('../../../components/GamePreScreen', () => ({
  default: ({ title, onStart }: { title: string; onStart: () => void }) => (
    <div data-testid="pre-screen">
      <span>{title}</span>
      <button onClick={onStart}>Start Game</button>
    </div>
  ),
}));

describe('WordMatchPage', () => {
  it('renders pre-screen initially', () => {
    render(<WordMatchPage />);
    expect(screen.getByTestId('pre-screen')).toBeInTheDocument();
  });

  it('renders Word Match title on pre-screen', () => {
    render(<WordMatchPage />);
    expect(screen.getByText('Word Match')).toBeInTheDocument();
  });

  it('renders Start Game button', () => {
    render(<WordMatchPage />);
    expect(screen.getByText('Start Game')).toBeInTheDocument();
  });

  it('renders without crashing', () => {
    const { container } = render(<WordMatchPage />);
    expect(container.firstChild).toBeDefined();
  });
});

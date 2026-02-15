import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import WordContextPage from '../../WordContextPage';

vi.mock('../../components/ContextParagraph', () => ({ default: () => <div data-testid="paragraph">Paragraph</div> }));
vi.mock('../../components/ContextInput', () => ({ default: () => <div data-testid="context-input">Input</div> }));
vi.mock('../../components/ContextFeedback', () => ({ default: () => <div data-testid="context-feedback">Feedback</div> }));
vi.mock('../../../components/GamePreScreen', () => ({
  default: ({ title, onStart }: { title: string; onStart: () => void }) => (
    <div data-testid="pre-screen">
      <span>{title}</span>
      <button onClick={onStart}>Start Game</button>
    </div>
  ),
}));

describe('WordContextPage', () => {
  it('renders pre-screen initially', () => {
    render(<WordContextPage />);
    expect(screen.getByTestId('pre-screen')).toBeInTheDocument();
  });

  it('renders Word Context title on pre-screen', () => {
    render(<WordContextPage />);
    expect(screen.getByText('Word Context')).toBeInTheDocument();
  });

  it('renders Start Game button', () => {
    render(<WordContextPage />);
    expect(screen.getByText('Start Game')).toBeInTheDocument();
  });

  it('renders without crashing', () => {
    const { container } = render(<WordContextPage />);
    expect(container.firstChild).toBeDefined();
  });
});

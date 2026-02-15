import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import StoryBuilderPage from '../../StoryBuilderPage';

vi.mock('../../components/GenreSelector', () => ({
  default: ({ onSelect }: { onSelect: (g: string) => void }) => (
    <div data-testid="genre-selector">
      <button onClick={() => onSelect('adventure')}>Adventure</button>
      <button onClick={() => onSelect('mystery')}>Mystery</button>
    </div>
  ),
}));
vi.mock('../../components/StoryDisplay', () => ({ default: () => <div data-testid="story-display">Story</div> }));
vi.mock('../../components/StoryWritingArea', () => ({ default: () => <div data-testid="writing-area">Write</div> }));
vi.mock('../../components/StoryRoundScore', () => ({ default: () => <div data-testid="round-score">Score</div> }));
vi.mock('../../components/StoryComplete', () => ({ default: () => <div data-testid="story-complete">Complete</div> }));

describe('StoryBuilderPage', () => {
  it('renders genre selector initially', () => {
    render(<StoryBuilderPage />);
    expect(screen.getByTestId('genre-selector')).toBeInTheDocument();
  });

  it('renders genre options', () => {
    render(<StoryBuilderPage />);
    expect(screen.getByText('Adventure')).toBeInTheDocument();
    expect(screen.getByText('Mystery')).toBeInTheDocument();
  });

  it('renders without crashing', () => {
    const { container } = render(<StoryBuilderPage />);
    expect(container.firstChild).toBeDefined();
  });
});

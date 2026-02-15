import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import ReviewSessionPage from '../../ReviewSessionPage';
import { useReviewStore } from '@/stores/useReviewStore';
import { createMockWord } from '@/test/utils';

// Mock react-router-dom hooks
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ sessionId: 'ses-1' }),
    useNavigate: () => mockNavigate,
    useLocation: () => ({ state: { sessionType: 'review' } }),
  };
});

// Mock child components
vi.mock('../components/SessionTopBar', () => ({
  default: ({ currentIndex, total, onQuit }: { currentIndex: number; total: number; onQuit: () => void }) => (
    <div data-testid="session-top-bar">
      <span data-testid="word-counter">{currentIndex + 1}/{total}</span>
      <button data-testid="quit-btn" onClick={onQuit}>Quit</button>
    </div>
  ),
}));
vi.mock('../components/SessionProgressBar', () => ({
  default: ({ progress }: { progress: number }) => <div data-testid="session-progress" data-progress={progress} />,
}));
vi.mock('../components/FlashCardContainer', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div data-testid="flashcard-container">{children}</div>,
}));
vi.mock('../components/FlashCard', () => ({
  default: ({ word, onFlip }: { word: { original_word: string }; onFlip: () => void }) => (
    <div data-testid="flashcard" onClick={onFlip}>{word.original_word}</div>
  ),
}));
vi.mock('../components/QualityRating', () => ({
  default: ({ onRate }: { onRate: (q: number) => void }) => (
    <div data-testid="quality-rating">
      <button data-testid="rate-good" onClick={() => onRate(3)}>Good</button>
    </div>
  ),
}));
vi.mock('../components/ComboIndicator', () => ({
  default: () => <div data-testid="combo-indicator" />,
}));
vi.mock('../components/ComboBreakEffect', () => ({
  default: () => <div data-testid="combo-break" />,
}));
vi.mock('../components/XPGainPopup', () => ({
  default: () => <div data-testid="xp-popup" />,
}));

describe('ReviewSessionPage', () => {
  const words = [
    createMockWord({ id: 'w1', original_word: 'hello' }),
    createMockWord({ id: 'w2', original_word: 'world' }),
  ];

  beforeEach(() => {
    mockNavigate.mockClear();
    useReviewStore.getState().reset();
    useReviewStore.getState().setWords(words);
  });

  it('renders session top bar', () => {
    render(<ReviewSessionPage />);
    expect(screen.getByTestId('session-top-bar')).toBeInTheDocument();
  });

  it('renders session progress bar', () => {
    render(<ReviewSessionPage />);
    expect(screen.getByTestId('session-progress')).toBeInTheDocument();
  });

  it('renders flashcard with current word', () => {
    render(<ReviewSessionPage />);
    expect(screen.getByTestId('flashcard')).toBeInTheDocument();
    expect(screen.getByText('hello')).toBeInTheDocument();
  });

  it('renders combo indicator', () => {
    render(<ReviewSessionPage />);
    expect(screen.getByTestId('combo-indicator')).toBeInTheDocument();
  });

  it('shows word counter in top bar', () => {
    render(<ReviewSessionPage />);
    expect(screen.getByTestId('word-counter')).toHaveTextContent('1/2');
  });

  it('shows loading when no words loaded', () => {
    useReviewStore.getState().setWords([]);
    render(<ReviewSessionPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });
});

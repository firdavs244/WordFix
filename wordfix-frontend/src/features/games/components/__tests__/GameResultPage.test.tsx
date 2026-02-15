import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import GameResultPage from '../../GameResultPage';

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ gameId: 'speed-round' }),
    useSearchParams: () => [new URLSearchParams('correct=4&total=5&time=45&xp=50')],
  };
});

describe('GameResultPage', () => {
  it('renders the score percentage', () => {
    render(<GameResultPage />);
    expect(screen.getByText('80%')).toBeInTheDocument();
  });

  it('renders correct answers stat', () => {
    render(<GameResultPage />);
    expect(screen.getByText('4')).toBeInTheDocument();
  });

  it('renders wrong answers stat', () => {
    render(<GameResultPage />);
    // wrong = total - correct = 5 - 4 = 1
    const ones = screen.getAllByText('1');
    expect(ones.length).toBeGreaterThanOrEqual(1);
  });

  it('renders Play Again link', () => {
    render(<GameResultPage />);
    expect(screen.getByText('Play Again')).toBeInTheDocument();
  });

  it('renders Dashboard link', () => {
    render(<GameResultPage />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('Play Again links to the correct game route', () => {
    render(<GameResultPage />);
    const link = screen.getByText('Play Again').closest('a');
    expect(link).toHaveAttribute('href', '/games/speed-round');
  });
});

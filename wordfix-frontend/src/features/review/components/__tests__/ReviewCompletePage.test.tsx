import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@/test/utils';
import { fireEvent } from '@testing-library/react';
import ReviewCompletePage from '../../ReviewCompletePage';

const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ sessionId: 'ses-1' }),
    useNavigate: () => mockNavigate,
  };
});

vi.mock('../CompletionCelebration', () => ({
  default: ({ accuracy }: { accuracy: number }) => <div data-testid="celebration" data-accuracy={accuracy} />,
}));
vi.mock('../CompletionStats', () => ({
  default: ({ total, correct, accuracy }: { total: number; correct: number; accuracy: number }) => (
    <div data-testid="completion-stats">
      <span data-testid="stat-total">{total}</span>
      <span data-testid="stat-correct">{correct}</span>
      <span data-testid="stat-accuracy">{accuracy}</span>
    </div>
  ),
}));
vi.mock('../CompletionActions', () => ({
  default: ({ onDashboard, onReviewAgain }: { onDashboard: () => void; onReviewAgain: () => void }) => (
    <div data-testid="completion-actions">
      <button data-testid="go-dashboard" onClick={onDashboard}>Dashboard</button>
      <button data-testid="go-review" onClick={onReviewAgain}>Review Again</button>
    </div>
  ),
}));

describe('ReviewCompletePage', () => {
  beforeEach(() => mockNavigate.mockClear());

  it('renders celebration component', async () => {
    render(<ReviewCompletePage />);
    expect(screen.getByTestId('celebration')).toBeInTheDocument();
  });

  it('renders completion stats component', async () => {
    render(<ReviewCompletePage />);
    expect(screen.getByTestId('completion-stats')).toBeInTheDocument();
  });

  it('renders completion actions component', () => {
    render(<ReviewCompletePage />);
    expect(screen.getByTestId('completion-actions')).toBeInTheDocument();
  });

  it('navigates to dashboard when Dashboard button clicked', () => {
    render(<ReviewCompletePage />);
    fireEvent.click(screen.getByTestId('go-dashboard'));
    expect(mockNavigate).toHaveBeenCalledWith('/');
  });

  it('navigates to review when Review Again button clicked', () => {
    render(<ReviewCompletePage />);
    fireEvent.click(screen.getByTestId('go-review'));
    expect(mockNavigate).toHaveBeenCalledWith('/review');
  });

  it('passes accuracy as 0 when session data is not loaded yet', () => {
    render(<ReviewCompletePage />);
    expect(screen.getByTestId('stat-accuracy')).toHaveTextContent('0');
  });
});

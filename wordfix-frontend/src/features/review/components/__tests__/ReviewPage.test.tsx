import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import ReviewPage from '../../ReviewPage';

vi.mock('../ReviewStats', () => ({ default: () => <div data-testid="review-stats">Stats</div> }));
vi.mock('../SessionTypeCards', () => ({ default: () => <div data-testid="session-type-cards">Cards</div> }));
vi.mock('../DueWordsPreview', () => ({ default: () => <div data-testid="due-words-preview">Preview</div> }));

describe('ReviewPage', () => {
  it('renders page header with title "Review"', () => {
    render(<ReviewPage />);
    expect(screen.getByText('Review')).toBeInTheDocument();
  });

  it('renders description text', () => {
    render(<ReviewPage />);
    expect(screen.getByText('Master your vocabulary with spaced repetition')).toBeInTheDocument();
  });

  it('renders ReviewStats component', () => {
    render(<ReviewPage />);
    expect(screen.getByTestId('review-stats')).toBeInTheDocument();
  });

  it('renders SessionTypeCards component', () => {
    render(<ReviewPage />);
    expect(screen.getByTestId('session-type-cards')).toBeInTheDocument();
  });

  it('renders DueWordsPreview component', () => {
    render(<ReviewPage />);
    expect(screen.getByTestId('due-words-preview')).toBeInTheDocument();
  });
});

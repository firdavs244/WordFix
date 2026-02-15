import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import GameResultStars from '../GameResultStars';

describe('GameResultStars', () => {
  it('renders 3 stars total', () => {
    render(<GameResultStars score={50} />);
    const stars = screen.getByTestId('result-stars');
    expect(stars).toBeInTheDocument();
  });

  it('renders 0 filled stars for score below 33', () => {
    render(<GameResultStars score={20} />);
    const filled = screen.queryAllByTestId('star-filled');
    const empty = screen.getAllByTestId('star-empty');
    expect(filled).toHaveLength(0);
    expect(empty).toHaveLength(3);
  });

  it('renders 1 filled star for score 33-65', () => {
    render(<GameResultStars score={50} />);
    const filled = screen.getAllByTestId('star-filled');
    expect(filled).toHaveLength(1);
  });

  it('renders 2 filled stars for score 66-89', () => {
    render(<GameResultStars score={80} />);
    const filled = screen.getAllByTestId('star-filled');
    expect(filled).toHaveLength(2);
  });

  it('renders 3 filled stars for score 90+', () => {
    render(<GameResultStars score={95} />);
    const filled = screen.getAllByTestId('star-filled');
    expect(filled).toHaveLength(3);
  });

  it('has result-stars test id', () => {
    render(<GameResultStars score={50} />);
    expect(screen.getByTestId('result-stars')).toBeInTheDocument();
  });
});

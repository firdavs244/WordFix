import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import GamesPage from '../../GamesPage';

describe('GamesPage', () => {
  it('renders page header with "Games"', () => {
    render(<GamesPage />);
    expect(screen.getByText('Games')).toBeInTheDocument();
  });

  it('renders description text', () => {
    render(<GamesPage />);
    expect(screen.getByText('Learn through play with 5 fun game modes')).toBeInTheDocument();
  });

  it('renders all 5 game cards', () => {
    render(<GamesPage />);
    expect(screen.getByText('Speed Round')).toBeInTheDocument();
    expect(screen.getByText('Word Match')).toBeInTheDocument();
    expect(screen.getByText('Word Context')).toBeInTheDocument();
    expect(screen.getByText('Story Builder')).toBeInTheDocument();
    expect(screen.getByText('Listening')).toBeInTheDocument();
  });

  it('renders game descriptions', () => {
    render(<GamesPage />);
    expect(screen.getByText('Translate words against the clock')).toBeInTheDocument();
    expect(screen.getByText('Match words with their translations')).toBeInTheDocument();
  });

  it('renders navigation links for each game', () => {
    render(<GamesPage />);
    const links = screen.getAllByRole('link');
    expect(links.length).toBe(5);
  });

  it('links have correct routes', () => {
    render(<GamesPage />);
    const links = screen.getAllByRole('link');
    const hrefs = links.map((l) => l.getAttribute('href'));
    expect(hrefs).toContain('/games/speed-round');
    expect(hrefs).toContain('/games/word-match');
    expect(hrefs).toContain('/games/word-context');
    expect(hrefs).toContain('/games/story-builder');
    expect(hrefs).toContain('/games/listening');
  });
});

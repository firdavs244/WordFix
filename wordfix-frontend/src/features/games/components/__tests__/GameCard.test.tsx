import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import { Zap } from 'lucide-react';
import GameCard from '../GameCard';

const props = {
  id: 'speed-round',
  title: 'Speed Round',
  description: 'Translate words against the clock',
  icon: Zap,
  gradient: 'from-amber-500/10 to-yellow-500/5',
  iconGradient: 'from-amber-500 to-yellow-500',
  route: '/games/speed-round',
};

describe('GameCard', () => {
  it('renders the game title', () => {
    render(<GameCard {...props} />);
    expect(screen.getByText('Speed Round')).toBeInTheDocument();
  });

  it('renders the game description', () => {
    render(<GameCard {...props} />);
    expect(screen.getByText('Translate words against the clock')).toBeInTheDocument();
  });

  it('renders a link to the game route', () => {
    render(<GameCard {...props} />);
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', '/games/speed-round');
  });

  it('renders best score when provided', () => {
    render(<GameCard {...props} bestScore={95} />);
    expect(screen.getByText('Best: 95%')).toBeInTheDocument();
  });

  it('does not render best score when not provided', () => {
    render(<GameCard {...props} />);
    expect(screen.queryByText(/Best:/)).not.toBeInTheDocument();
  });

  it('renders the card without crashing', () => {
    const { container } = render(<GameCard {...props} />);
    expect(container.firstChild).toBeDefined();
  });
});

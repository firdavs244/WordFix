import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import GameComboIndicator from '../GameComboIndicator';

describe('GameComboIndicator', () => {
  it('does not render when combo is 0', () => {
    render(<GameComboIndicator combo={0} multiplier={1} />);
    expect(screen.queryByTestId('combo-indicator')).not.toBeInTheDocument();
  });

  it('does not render when combo is 1', () => {
    render(<GameComboIndicator combo={1} multiplier={1.1} />);
    expect(screen.queryByTestId('combo-indicator')).not.toBeInTheDocument();
  });

  it('renders combo when above 1', () => {
    render(<GameComboIndicator combo={5} multiplier={1.5} />);
    expect(screen.getByTestId('combo-indicator')).toBeInTheDocument();
  });

  it('displays combo count', () => {
    render(<GameComboIndicator combo={7} multiplier={1.7} />);
    expect(screen.getByText('7')).toBeInTheDocument();
  });

  it('displays multiplier', () => {
    render(<GameComboIndicator combo={3} multiplier={1.3} />);
    expect(screen.getByText('×1.3')).toBeInTheDocument();
  });
});

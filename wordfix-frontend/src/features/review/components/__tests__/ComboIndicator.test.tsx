import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import ComboIndicator from '../ComboIndicator';

describe('ComboIndicator', () => {
  it('does not render when combo is 0', () => {
    render(<ComboIndicator combo={0} multiplier={1} />);
    expect(screen.queryByTestId('combo-indicator')).not.toBeInTheDocument();
  });

  it('does not render when combo is 1', () => {
    render(<ComboIndicator combo={1} multiplier={1} />);
    expect(screen.queryByTestId('combo-indicator')).not.toBeInTheDocument();
  });

  it('renders when combo is 2 or more', () => {
    render(<ComboIndicator combo={2} multiplier={1.2} />);
    expect(screen.getByTestId('combo-indicator')).toBeInTheDocument();
  });

  it('displays the combo count', () => {
    render(<ComboIndicator combo={5} multiplier={1.5} />);
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('displays the multiplier', () => {
    render(<ComboIndicator combo={3} multiplier={1.5} />);
    expect(screen.getByText('×1.5')).toBeInTheDocument();
  });

  it('applies yellow style for low combo (< 5)', () => {
    render(<ComboIndicator combo={3} multiplier={1.3} />);
    const el = screen.getByTestId('combo-indicator');
    expect(el.className).toContain('yellow');
  });

  it('applies orange style for combo >= 5', () => {
    render(<ComboIndicator combo={7} multiplier={1.5} />);
    const el = screen.getByTestId('combo-indicator');
    expect(el.className).toContain('orange');
  });

  it('applies primary style for combo >= 20', () => {
    render(<ComboIndicator combo={25} multiplier={3} />);
    const el = screen.getByTestId('combo-indicator');
    expect(el.className).toContain('primary');
  });
});

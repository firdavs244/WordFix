import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import SpeedRoundWord from '../SpeedRoundWord';

describe('SpeedRoundWord', () => {
  it('renders the word text', () => {
    render(<SpeedRoundWord word="hello" />);
    expect(screen.getByText('hello')).toBeInTheDocument();
  });

  it('renders instruction text', () => {
    render(<SpeedRoundWord word="hello" />);
    expect(screen.getByText('Choose the correct translation')).toBeInTheDocument();
  });

  it('updates when word changes', () => {
    const { rerender } = render(<SpeedRoundWord word="hello" />);
    rerender(<SpeedRoundWord word="world" />);
    expect(screen.getByText('world')).toBeInTheDocument();
  });
});

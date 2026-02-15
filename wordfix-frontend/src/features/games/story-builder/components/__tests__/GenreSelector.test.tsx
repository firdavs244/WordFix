import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import GenreSelector from '../GenreSelector';

describe('GenreSelector', () => {
  const onSelect = vi.fn();

  beforeEach(() => onSelect.mockClear());

  it('renders the heading', () => {
    render(<GenreSelector onSelect={onSelect} isLoading={false} />);
    expect(screen.getByText('Choose a Genre')).toBeInTheDocument();
  });

  it('renders all 6 genre cards', () => {
    render(<GenreSelector onSelect={onSelect} isLoading={false} />);
    expect(screen.getByText('adventure')).toBeInTheDocument();
    expect(screen.getByText('mystery')).toBeInTheDocument();
    expect(screen.getByText('romance')).toBeInTheDocument();
    expect(screen.getByText('sci-fi')).toBeInTheDocument();
    expect(screen.getByText('fantasy')).toBeInTheDocument();
    expect(screen.getByText('comedy')).toBeInTheDocument();
  });

  it('calls onSelect when a genre is clicked', async () => {
    const user = userEvent.setup();
    render(<GenreSelector onSelect={onSelect} isLoading={false} />);
    await user.click(screen.getByText('adventure'));
    expect(onSelect).toHaveBeenCalledWith('adventure');
  });

  it('renders description text', () => {
    render(<GenreSelector onSelect={onSelect} isLoading={false} />);
    expect(screen.getByText('Pick a genre for your AI-collaborative story')).toBeInTheDocument();
  });
});

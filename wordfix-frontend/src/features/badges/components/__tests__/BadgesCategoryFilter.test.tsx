import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import BadgesCategoryFilter from '../BadgesCategoryFilter';

describe('BadgesCategoryFilter', () => {
  it('renders all category chips', () => {
    render(<BadgesCategoryFilter activeCategory="all" onChange={vi.fn()} />);
    expect(screen.getByText('All')).toBeInTheDocument();
    expect(screen.getByText('Words')).toBeInTheDocument();
    expect(screen.getByText('Streak')).toBeInTheDocument();
    expect(screen.getByText('Tests')).toBeInTheDocument();
    expect(screen.getByText('Games')).toBeInTheDocument();
    expect(screen.getByText('Mastery')).toBeInTheDocument();
    expect(screen.getByText('Level')).toBeInTheDocument();
  });

  it('highlights active category', () => {
    render(<BadgesCategoryFilter activeCategory="words" onChange={vi.fn()} />);
    const wordsChip = screen.getByText('Words');
    expect(wordsChip).toHaveClass('font-semibold');
  });

  it('calls onChange when chip clicked', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();
    render(<BadgesCategoryFilter activeCategory="all" onChange={onChange} />);
    await user.click(screen.getByText('Streak'));
    expect(onChange).toHaveBeenCalledWith('streak');
  });

  it('starts with "All" selected by default', () => {
    render(<BadgesCategoryFilter activeCategory="all" onChange={vi.fn()} />);
    const allChip = screen.getByText('All');
    expect(allChip).toHaveClass('font-semibold');
  });
});

import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import QualityRating from '../QualityRating';
import type { ReviewQuality } from '@/types';

describe('QualityRating', () => {
  const onRate = vi.fn();

  beforeEach(() => onRate.mockClear());

  it('renders six quality buttons', () => {
    render(<QualityRating onRate={onRate} />);
    expect(screen.getByText('Again')).toBeInTheDocument();
    expect(screen.getByText('Hard')).toBeInTheDocument();
    expect(screen.getByText('Difficult')).toBeInTheDocument();
    expect(screen.getByText('Good')).toBeInTheDocument();
    expect(screen.getByText('Easy')).toBeInTheDocument();
    expect(screen.getByText('Perfect')).toBeInTheDocument();
  });

  it('calls onRate with 0 when Again clicked', async () => {
    const user = userEvent.setup();
    render(<QualityRating onRate={onRate} />);
    await user.click(screen.getByText('Again'));
    expect(onRate).toHaveBeenCalledWith(0);
  });

  it('calls onRate with 5 when Perfect clicked', async () => {
    const user = userEvent.setup();
    render(<QualityRating onRate={onRate} />);
    await user.click(screen.getByText('Perfect'));
    expect(onRate).toHaveBeenCalledWith(5);
  });

  it('calls onRate via keyboard shortcut 1 → quality 0', async () => {
    const user = userEvent.setup();
    render(<QualityRating onRate={onRate} />);
    await user.keyboard('1');
    expect(onRate).toHaveBeenCalledWith(0);
  });

  it('calls onRate via keyboard shortcut 4 → quality 3', async () => {
    const user = userEvent.setup();
    render(<QualityRating onRate={onRate} />);
    await user.keyboard('4');
    expect(onRate).toHaveBeenCalledWith(3);
  });

  it('calls onRate via keyboard shortcut 6 → quality 5', async () => {
    const user = userEvent.setup();
    render(<QualityRating onRate={onRate} />);
    await user.keyboard('6');
    expect(onRate).toHaveBeenCalledWith(5);
  });

  it('renders emojis for each quality level', () => {
    render(<QualityRating onRate={onRate} />);
    expect(screen.getByText('😫')).toBeInTheDocument();
    expect(screen.getByText('🤩')).toBeInTheDocument();
  });

  it('renders keyboard shortcut labels', () => {
    render(<QualityRating onRate={onRate} />);
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('6')).toBeInTheDocument();
  });
});

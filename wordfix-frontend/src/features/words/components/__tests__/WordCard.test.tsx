import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import WordCard from '../WordCard';
import { createMockWord } from '@/test/utils';

// Mock MouseTiltCard to just render children
vi.mock('@/features/dashboard/components/MouseTiltCard', () => ({
  default: ({ children }: { children: React.ReactNode }) => <div data-testid="tilt-card">{children}</div>,
}));

describe('WordCard', () => {
  const onDelete = vi.fn();

  it('renders word and translation', () => {
    const word = createMockWord({ original_word: 'apple', translation: 'manzana' });
    render(<WordCard word={word} onDelete={onDelete} />);
    expect(screen.getByText('apple')).toBeInTheDocument();
    expect(screen.getByText('manzana')).toBeInTheDocument();
  });

  it('renders definition when provided', () => {
    const word = createMockWord({ definition: 'A round fruit' });
    render(<WordCard word={word} onDelete={onDelete} />);
    expect(screen.getByText('A round fruit')).toBeInTheDocument();
  });

  it('does not render definition when empty', () => {
    const word = createMockWord({ definition: '' });
    render(<WordCard word={word} onDelete={onDelete} />);
    expect(screen.queryByText('A greeting')).not.toBeInTheDocument();
  });

  it('has accessible article role with word name', () => {
    const word = createMockWord({ original_word: 'cat' });
    render(<WordCard word={word} onDelete={onDelete} />);
    expect(screen.getByRole('article')).toHaveAttribute('aria-label', 'Word: cat');
  });

  it('renders delete button with correct aria-label', () => {
    const word = createMockWord({ original_word: 'dog' });
    render(<WordCard word={word} onDelete={onDelete} />);
    expect(screen.getByLabelText('Delete dog')).toBeInTheDocument();
  });

  it('calls onDelete with word id when delete button is clicked', async () => {
    const { userEvent: ue } = await import('@testing-library/user-event');
    const user = ue.setup();
    const word = createMockWord({ id: 'word-42', original_word: 'test' });
    render(<WordCard word={word} onDelete={onDelete} />);
    await user.click(screen.getByLabelText('Delete test'));
    expect(onDelete).toHaveBeenCalledWith('word-42');
  });

  it('applies success border for easy difficulty', () => {
    const word = createMockWord({ difficulty_level: 'easy' });
    render(<WordCard word={word} onDelete={onDelete} />);
    const article = screen.getByRole('article');
    expect(article.className).toContain('border-l-success');
  });

  it('applies accent border for medium difficulty', () => {
    const word = createMockWord({ difficulty_level: 'medium' });
    render(<WordCard word={word} onDelete={onDelete} />);
    const article = screen.getByRole('article');
    expect(article.className).toContain('border-l-accent');
  });

  it('applies destructive border for hard difficulty', () => {
    const word = createMockWord({ difficulty_level: 'hard' });
    render(<WordCard word={word} onDelete={onDelete} />);
    const article = screen.getByRole('article');
    expect(article.className).toContain('border-l-destructive');
  });
});

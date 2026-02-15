import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import { createMockWord } from '@/test/utils';
import FlashCard from '../FlashCard';

describe('FlashCard', () => {
  const word = createMockWord({ original_word: 'sun', translation: 'sol', definition: 'A star', pronunciation: 'sʌn' });
  const onFlip = vi.fn();

  beforeEach(() => onFlip.mockClear());

  it('renders the FlashCardFront with word', () => {
    render(<FlashCard word={word} isFlipped={false} onFlip={onFlip} />);
    expect(screen.getByText('sun')).toBeInTheDocument();
  });

  it('renders the FlashCardBack with translation', () => {
    render(<FlashCard word={word} isFlipped={true} onFlip={onFlip} />);
    expect(screen.getByText('sol')).toBeInTheDocument();
  });

  it('calls onFlip when clicked', async () => {
    const user = userEvent.setup();
    render(<FlashCard word={word} isFlipped={false} onFlip={onFlip} />);
    const card = screen.getByRole('button');
    await user.click(card);
    expect(onFlip).toHaveBeenCalledTimes(1);
  });

  it('has accessible button role', () => {
    render(<FlashCard word={word} isFlipped={false} onFlip={onFlip} />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('has appropriate aria-label for front', () => {
    render(<FlashCard word={word} isFlipped={false} onFlip={onFlip} />);
    expect(screen.getByRole('button')).toHaveAttribute('aria-label', 'Flash card front');
  });

  it('has appropriate aria-label for back', () => {
    render(<FlashCard word={word} isFlipped={true} onFlip={onFlip} />);
    expect(screen.getByRole('button')).toHaveAttribute('aria-label', 'Flash card back');
  });

  it('renders definition on the back', () => {
    render(<FlashCard word={word} isFlipped={true} onFlip={onFlip} />);
    expect(screen.getByText('A star')).toBeInTheDocument();
  });

  it('renders pronunciation on the front', () => {
    render(<FlashCard word={word} isFlipped={false} onFlip={onFlip} />);
    expect(screen.getByText('/sʌn/')).toBeInTheDocument();
  });
});

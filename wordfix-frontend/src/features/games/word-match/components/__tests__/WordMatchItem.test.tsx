import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import WordMatchItem from '../WordMatchItem';

describe('WordMatchItem', () => {
  const onClick = vi.fn();

  beforeEach(() => onClick.mockClear());

  it('renders the text', () => {
    render(<WordMatchItem text="hello" type="word" isSelected={false} isMatched={false} isWrong={false} onClick={onClick} />);
    expect(screen.getByText('hello')).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    render(<WordMatchItem text="hello" type="word" isSelected={false} isMatched={false} isWrong={false} onClick={onClick} />);
    await user.click(screen.getByTestId('match-word-hello'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when matched', () => {
    render(<WordMatchItem text="hello" type="word" isSelected={false} isMatched={true} isWrong={false} onClick={onClick} />);
    expect(screen.getByTestId('match-word-hello')).toBeDisabled();
  });

  it('has correct test id for word type', () => {
    render(<WordMatchItem text="hello" type="word" isSelected={false} isMatched={false} isWrong={false} onClick={onClick} />);
    expect(screen.getByTestId('match-word-hello')).toBeInTheDocument();
  });

  it('has correct test id for translation type', () => {
    render(<WordMatchItem text="hola" type="translation" isSelected={false} isMatched={false} isWrong={false} onClick={onClick} />);
    expect(screen.getByTestId('match-translation-hola')).toBeInTheDocument();
  });
});

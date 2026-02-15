import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ListeningFeedback from '../ListeningFeedback';

describe('ListeningFeedback', () => {
  const onNext = vi.fn();

  beforeEach(() => onNext.mockClear());

  it('renders Correct text when correct', () => {
    render(<ListeningFeedback isCorrect={true} correctAnswer="hello" onNext={onNext} />);
    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });

  it('renders Incorrect text when wrong', () => {
    render(<ListeningFeedback isCorrect={false} correctAnswer="hello" onNext={onNext} />);
    expect(screen.getByText('Incorrect')).toBeInTheDocument();
  });

  it('shows correct answer when wrong', () => {
    render(<ListeningFeedback isCorrect={false} correctAnswer="hello" onNext={onNext} />);
    expect(screen.getByText('hello')).toBeInTheDocument();
    expect(screen.getByText(/The word was:/)).toBeInTheDocument();
  });

  it('does not show correct answer when correct', () => {
    render(<ListeningFeedback isCorrect={true} correctAnswer="hello" onNext={onNext} />);
    expect(screen.queryByText(/The word was:/)).not.toBeInTheDocument();
  });

  it('renders Next button', () => {
    render(<ListeningFeedback isCorrect={true} correctAnswer="hello" onNext={onNext} />);
    expect(screen.getByText('Next')).toBeInTheDocument();
  });

  it('calls onNext when button clicked', async () => {
    const user = userEvent.setup();
    render(<ListeningFeedback isCorrect={true} correctAnswer="hello" onNext={onNext} />);
    await user.click(screen.getByText('Next'));
    expect(onNext).toHaveBeenCalledTimes(1);
  });
});

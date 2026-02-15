import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ContextFeedback from '../ContextFeedback';

describe('ContextFeedback', () => {
  const onNext = vi.fn();

  beforeEach(() => onNext.mockClear());

  it('renders Correct text when correct', () => {
    render(<ContextFeedback isCorrect={true} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });

  it('renders Incorrect text when wrong', () => {
    render(<ContextFeedback isCorrect={false} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Incorrect')).toBeInTheDocument();
  });

  it('renders explanation when provided', () => {
    render(<ContextFeedback isCorrect={true} explanation="Good job!" onNext={onNext} isLast={false} />);
    expect(screen.getByText('Good job!')).toBeInTheDocument();
  });

  it('renders Next button when not last', () => {
    render(<ContextFeedback isCorrect={true} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Next')).toBeInTheDocument();
  });

  it('renders See Results button when last', () => {
    render(<ContextFeedback isCorrect={true} onNext={onNext} isLast={true} />);
    expect(screen.getByText('See Results')).toBeInTheDocument();
  });

  it('calls onNext when button clicked', async () => {
    const user = userEvent.setup();
    render(<ContextFeedback isCorrect={true} onNext={onNext} isLast={false} />);
    await user.click(screen.getByText('Next'));
    expect(onNext).toHaveBeenCalledTimes(1);
  });
});

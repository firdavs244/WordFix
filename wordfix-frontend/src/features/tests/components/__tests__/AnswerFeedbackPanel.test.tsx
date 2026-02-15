import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import AnswerFeedbackPanel from '../AnswerFeedbackPanel';

describe('AnswerFeedbackPanel', () => {
  const onNext = vi.fn();

  beforeEach(() => onNext.mockClear());

  it('renders Correct text when correct', () => {
    render(<AnswerFeedbackPanel isCorrect={true} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });

  it('renders Incorrect text when wrong', () => {
    render(<AnswerFeedbackPanel isCorrect={false} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Incorrect')).toBeInTheDocument();
  });

  it('shows correct answer when wrong', () => {
    render(<AnswerFeedbackPanel isCorrect={false} correctAnswer="hola" onNext={onNext} isLast={false} />);
    expect(screen.getByText('hola')).toBeInTheDocument();
  });

  it('shows explanation when provided', () => {
    render(<AnswerFeedbackPanel isCorrect={true} explanation="Well done!" onNext={onNext} isLast={false} />);
    expect(screen.getByText('Well done!')).toBeInTheDocument();
  });

  it('renders Next Question button when not last', () => {
    render(<AnswerFeedbackPanel isCorrect={true} onNext={onNext} isLast={false} />);
    expect(screen.getByText('Next Question')).toBeInTheDocument();
  });

  it('renders See Results button when last', () => {
    render(<AnswerFeedbackPanel isCorrect={true} onNext={onNext} isLast={true} />);
    expect(screen.getByText('See Results')).toBeInTheDocument();
  });

  it('calls onNext when button clicked', async () => {
    const user = userEvent.setup();
    render(<AnswerFeedbackPanel isCorrect={true} onNext={onNext} isLast={false} />);
    await user.click(screen.getByText('Next Question'));
    expect(onNext).toHaveBeenCalledTimes(1);
  });

  it('has answer-feedback test id', () => {
    render(<AnswerFeedbackPanel isCorrect={true} onNext={onNext} isLast={false} />);
    expect(screen.getByTestId('answer-feedback')).toBeInTheDocument();
  });
});

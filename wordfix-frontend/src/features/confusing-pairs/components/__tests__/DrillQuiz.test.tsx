import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import { DrillQuiz } from '../../components/DrillQuiz';

const question = {
  sentence: 'The rain will ___ the game.',
  correct_answer: 'affect',
  wrong_answer: 'effect',
  explanation: 'Affect is used as a verb here.',
};

describe('DrillQuiz', () => {
  const onAnswer = vi.fn();
  const onNext = vi.fn();

  it('renders question sentence', () => {
    render(<DrillQuiz question={question} quizIndex={0} totalQuestions={3} selectedAnswer={null} answered={false} onAnswer={onAnswer} onNext={onNext} />);
    expect(screen.getByText(/the rain will/i)).toBeInTheDocument();
  });

  it('shows question counter', () => {
    render(<DrillQuiz question={question} quizIndex={0} totalQuestions={3} selectedAnswer={null} answered={false} onAnswer={onAnswer} onNext={onNext} />);
    expect(screen.getByText('Question 1 of 3')).toBeInTheDocument();
  });

  it('renders answer options', () => {
    render(<DrillQuiz question={question} quizIndex={0} totalQuestions={3} selectedAnswer={null} answered={false} onAnswer={onAnswer} onNext={onNext} />);
    expect(screen.getByText('affect')).toBeInTheDocument();
    expect(screen.getByText('effect')).toBeInTheDocument();
  });

  it('calls onAnswer when an option is clicked', async () => {
    const user = userEvent.setup();
    render(<DrillQuiz question={question} quizIndex={0} totalQuestions={3} selectedAnswer={null} answered={false} onAnswer={onAnswer} onNext={onNext} />);
    await user.click(screen.getByText('affect'));
    expect(onAnswer).toHaveBeenCalledWith('affect');
  });

  it('shows explanation after answering', () => {
    render(<DrillQuiz question={question} quizIndex={0} totalQuestions={3} selectedAnswer="affect" answered={true} onAnswer={onAnswer} onNext={onNext} />);
    expect(screen.getByText('Affect is used as a verb here.')).toBeInTheDocument();
  });
});

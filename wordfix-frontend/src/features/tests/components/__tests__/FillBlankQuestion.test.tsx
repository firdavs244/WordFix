import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import FillBlankQuestion from '../FillBlankQuestion';

describe('FillBlankQuestion', () => {
  const onSubmit = vi.fn();
  const sentence = 'She said ___ to everyone.';

  beforeEach(() => onSubmit.mockClear());

  it('renders the sentence with blank', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    expect(screen.getByText(/She said/)).toBeInTheDocument();
    expect(screen.getByText(/to everyone/)).toBeInTheDocument();
  });

  it('renders an input field with accessible label', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    expect(screen.getByLabelText('Answer input')).toBeInTheDocument();
  });

  it('renders submit button', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    expect(screen.getByLabelText('Submit answer')).toBeInTheDocument();
  });

  it('submit button is disabled when input is empty', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    expect(screen.getByLabelText('Submit answer')).toBeDisabled();
  });

  it('calls onSubmit when button clicked with value', async () => {
    const user = userEvent.setup();
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    await user.type(screen.getByLabelText('Answer input'), 'hello');
    await user.click(screen.getByLabelText('Submit answer'));
    expect(onSubmit).toHaveBeenCalledWith('hello');
  });

  it('calls onSubmit on Enter key press', async () => {
    const user = userEvent.setup();
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={false} />);
    await user.type(screen.getByLabelText('Answer input'), 'hello{Enter}');
    expect(onSubmit).toHaveBeenCalledWith('hello');
  });

  it('hides input when answered', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={true} userAnswer="hello" isCorrect={true} correctAnswer="hello" />);
    expect(screen.queryByLabelText('Answer input')).not.toBeInTheDocument();
  });

  it('shows correct answer when wrong', () => {
    render(<FillBlankQuestion sentence={sentence} onSubmit={onSubmit} answered={true} userAnswer="goodbye" isCorrect={false} correctAnswer="hello" />);
    expect(screen.getByText(/Correct: hello/)).toBeInTheDocument();
  });
});

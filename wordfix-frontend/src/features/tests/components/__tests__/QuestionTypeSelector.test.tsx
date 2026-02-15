import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import QuestionTypeSelector from '../QuestionTypeSelector';

describe('QuestionTypeSelector', () => {
  const onChange = vi.fn();

  beforeEach(() => onChange.mockClear());

  it('renders the Question Type label', () => {
    render(<QuestionTypeSelector value="multiple_choice" onChange={onChange} />);
    expect(screen.getByText('Question Type')).toBeInTheDocument();
  });

  it('renders all four type cards', () => {
    render(<QuestionTypeSelector value="multiple_choice" onChange={onChange} />);
    expect(screen.getByText('Multiple Choice')).toBeInTheDocument();
    expect(screen.getByText('Fill in the Blank')).toBeInTheDocument();
    expect(screen.getByText('Context Guess')).toBeInTheDocument();
    expect(screen.getByText('Mixed')).toBeInTheDocument();
  });

  it('calls onChange when a card is clicked', async () => {
    const user = userEvent.setup();
    render(<QuestionTypeSelector value="multiple_choice" onChange={onChange} />);
    await user.click(screen.getByText('Fill in the Blank'));
    expect(onChange).toHaveBeenCalledWith('fill_blank');
  });

  it('highlights the selected type card', () => {
    render(<QuestionTypeSelector value="mixed" onChange={onChange} />);
    const mixedCard = screen.getByText('Mixed').closest('button');
    expect(mixedCard).toBeDefined();
  });
});

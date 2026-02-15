import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import MultipleChoiceQuestion from '../MultipleChoiceQuestion';

describe('MultipleChoiceQuestion', () => {
  const options = ['hola', 'mundo', 'casa', 'perro'];
  const onSelect = vi.fn();

  beforeEach(() => onSelect.mockClear());

  it('renders all four options', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={false} />);
    options.forEach((opt) => {
      expect(screen.getByText(opt)).toBeInTheDocument();
    });
  });

  it('renders letter prefixes A through D', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={false} />);
    expect(screen.getByText('A')).toBeInTheDocument();
    expect(screen.getByText('B')).toBeInTheDocument();
    expect(screen.getByText('C')).toBeInTheDocument();
    expect(screen.getByText('D')).toBeInTheDocument();
  });

  it('calls onSelect with index when option clicked', async () => {
    const user = userEvent.setup();
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={false} />);
    await user.click(screen.getByTestId('option-2'));
    expect(onSelect).toHaveBeenCalledWith(2);
  });

  it('does not call onSelect when answered', async () => {
    const user = userEvent.setup();
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={true} selectedIndex={0} correctIndex={0} />);
    await user.click(screen.getByTestId('option-1'));
    expect(onSelect).not.toHaveBeenCalled();
  });

  it('shows check icon on correct answer', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={true} selectedIndex={0} correctIndex={0} />);
    expect(screen.getByTestId('check-icon')).toBeInTheDocument();
  });

  it('shows x icon on wrong answer', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={true} selectedIndex={1} correctIndex={0} />);
    expect(screen.getByTestId('x-icon')).toBeInTheDocument();
  });

  it('shows both correct and wrong indicators when answer is wrong', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={true} selectedIndex={1} correctIndex={0} />);
    expect(screen.getByTestId('check-icon')).toBeInTheDocument();
    expect(screen.getByTestId('x-icon')).toBeInTheDocument();
  });

  it('has group role for accessibility', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={false} />);
    expect(screen.getByRole('group')).toBeInTheDocument();
  });

  it('disables all buttons when answered', () => {
    render(<MultipleChoiceQuestion options={options} onSelect={onSelect} answered={true} selectedIndex={0} correctIndex={0} />);
    const buttons = screen.getAllByRole('button');
    buttons.forEach((btn) => expect(btn).toBeDisabled());
  });
});

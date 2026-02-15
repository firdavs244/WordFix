import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@/test/utils';
import QuestionCountSlider from '../QuestionCountSlider';

describe('QuestionCountSlider', () => {
  const onChange = vi.fn();

  beforeEach(() => onChange.mockClear());

  it('renders the Questions label', () => {
    render(<QuestionCountSlider value={10} onChange={onChange} />);
    expect(screen.getByText('Questions')).toBeInTheDocument();
  });

  it('displays the current value', () => {
    render(<QuestionCountSlider value={15} onChange={onChange} />);
    expect(screen.getByText('15')).toBeInTheDocument();
  });

  it('renders range input with accessible label', () => {
    render(<QuestionCountSlider value={10} onChange={onChange} />);
    expect(screen.getByLabelText('Question count')).toBeInTheDocument();
  });

  it('renders tick marks', () => {
    render(<QuestionCountSlider value={10} onChange={onChange} />);
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('30')).toBeInTheDocument();
  });

  it('has correct min and max on range input', () => {
    render(<QuestionCountSlider value={10} onChange={onChange} />);
    const input = screen.getByLabelText('Question count');
    expect(input).toHaveAttribute('min', '5');
    expect(input).toHaveAttribute('max', '30');
  });
});

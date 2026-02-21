import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import DifficultySelector from '../DifficultySelector';

describe('DifficultySelector', () => {
  const onChange = vi.fn();

  beforeEach(() => onChange.mockClear());

  it('renders the Difficulty label', () => {
    render(<DifficultySelector value="medium" onChange={onChange} />);
    expect(screen.getByText('Difficulty')).toBeInTheDocument();
  });

  it('renders all four difficulty options', () => {
    render(<DifficultySelector value="medium" onChange={onChange} />);
    expect(screen.getByText('Easy')).toBeInTheDocument();
    expect(screen.getByText('Medium')).toBeInTheDocument();
    expect(screen.getByText('Hard')).toBeInTheDocument();
    expect(screen.getByText('Adaptive')).toBeInTheDocument();
  });

  it('calls onChange when a different option is clicked', async () => {
    const user = userEvent.setup();
    render(<DifficultySelector value="medium" onChange={onChange} />);
    await user.click(screen.getByText('Hard'));
    expect(onChange).toHaveBeenCalledWith('hard');
  });
});

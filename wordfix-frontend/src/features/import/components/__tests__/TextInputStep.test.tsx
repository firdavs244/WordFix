import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import TextInputStep from '../../components/TextInputStep';

describe('TextInputStep', () => {
  const onChange = vi.fn();

  it('renders textarea with placeholder', () => {
    render(<TextInputStep text="" onChange={onChange} />);
    expect(screen.getByPlaceholderText(/paste.*text/i)).toBeInTheDocument();
  });

  it('shows character count', () => {
    render(<TextInputStep text="hello" onChange={onChange} />);
    expect(screen.getByText('5/5000')).toBeInTheDocument();
  });

  it('calls onChange on input', async () => {
    const user = userEvent.setup();
    render(<TextInputStep text="" onChange={onChange} />);
    await user.type(screen.getByRole('textbox'), 'a');
    expect(onChange).toHaveBeenCalled();
  });
});

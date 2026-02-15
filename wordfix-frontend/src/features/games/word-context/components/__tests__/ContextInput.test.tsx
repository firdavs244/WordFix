import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ContextInput from '../ContextInput';

describe('ContextInput', () => {
  const onSubmit = vi.fn();

  beforeEach(() => onSubmit.mockClear());

  it('renders input with accessible label', () => {
    render(<ContextInput onSubmit={onSubmit} disabled={false} />);
    expect(screen.getByLabelText('Context answer input')).toBeInTheDocument();
  });

  it('renders submit button', () => {
    render(<ContextInput onSubmit={onSubmit} disabled={false} />);
    expect(screen.getByLabelText('Submit')).toBeInTheDocument();
  });

  it('calls onSubmit when typing and pressing Enter', async () => {
    const user = userEvent.setup();
    render(<ContextInput onSubmit={onSubmit} disabled={false} />);
    await user.type(screen.getByLabelText('Context answer input'), 'hello{Enter}');
    expect(onSubmit).toHaveBeenCalledWith('hello');
  });

  it('clears input after submit', async () => {
    const user = userEvent.setup();
    render(<ContextInput onSubmit={onSubmit} disabled={false} />);
    const input = screen.getByLabelText('Context answer input');
    await user.type(input, 'hello{Enter}');
    expect(input).toHaveValue('');
  });

  it('does not submit empty input', async () => {
    const user = userEvent.setup();
    render(<ContextInput onSubmit={onSubmit} disabled={false} />);
    await user.type(screen.getByLabelText('Context answer input'), '{Enter}');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('disables input when disabled prop is true', () => {
    render(<ContextInput onSubmit={onSubmit} disabled={true} />);
    expect(screen.getByLabelText('Context answer input')).toBeDisabled();
  });
});

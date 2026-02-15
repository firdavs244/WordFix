import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ListeningInput from '../ListeningInput';

describe('ListeningInput', () => {
  const onSubmit = vi.fn();

  beforeEach(() => onSubmit.mockClear());

  it('renders input with accessible label', () => {
    render(<ListeningInput onSubmit={onSubmit} disabled={false} />);
    expect(screen.getByLabelText('Listening answer')).toBeInTheDocument();
  });

  it('renders submit button', () => {
    render(<ListeningInput onSubmit={onSubmit} disabled={false} />);
    expect(screen.getByLabelText('Submit')).toBeInTheDocument();
  });

  it('calls onSubmit when typing and pressing Enter', async () => {
    const user = userEvent.setup();
    render(<ListeningInput onSubmit={onSubmit} disabled={false} />);
    await user.type(screen.getByLabelText('Listening answer'), 'hello{Enter}');
    expect(onSubmit).toHaveBeenCalledWith('hello');
  });

  it('does not submit empty input', async () => {
    const user = userEvent.setup();
    render(<ListeningInput onSubmit={onSubmit} disabled={false} />);
    await user.type(screen.getByLabelText('Listening answer'), '{Enter}');
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it('disables input when disabled prop is true', () => {
    render(<ListeningInput onSubmit={onSubmit} disabled={true} />);
    expect(screen.getByLabelText('Listening answer')).toBeDisabled();
  });
});

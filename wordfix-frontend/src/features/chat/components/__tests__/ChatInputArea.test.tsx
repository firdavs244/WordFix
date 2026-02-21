import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ChatInputArea from '../../components/ChatInputArea';

describe('ChatInputArea', () => {
  const onSend = vi.fn();

  it('renders textarea with placeholder', () => {
    render(<ChatInputArea onSend={onSend} disabled={false} />);
    expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
  });

  it('renders send button', () => {
    render(<ChatInputArea onSend={onSend} disabled={false} />);
    expect(screen.getByLabelText('Send message')).toBeInTheDocument();
  });

  it('disables send button when textarea is empty', () => {
    render(<ChatInputArea onSend={onSend} disabled={false} />);
    expect(screen.getByLabelText('Send message')).toBeDisabled();
  });

  it('calls onSend when clicking send button', async () => {
    const user = userEvent.setup();
    render(<ChatInputArea onSend={onSend} disabled={false} />);
    const textarea = screen.getByPlaceholderText(/type your message/i);
    await user.type(textarea, 'Hello world');
    await user.click(screen.getByLabelText('Send message'));
    expect(onSend).toHaveBeenCalledWith('Hello world');
  });
});

import { describe, it, expect } from 'vitest';
import { render, screen, createMockMessage } from '@/test/utils';
import ChatMessage from '../../components/ChatMessage';

describe('ChatMessage', () => {
  it('renders user message on the right', () => {
    const msg = createMockMessage({ role: 'user', content: 'Hi there!' });
    render(<ChatMessage message={msg} />);
    expect(screen.getByText('Hi there!')).toBeInTheDocument();
  });

  it('renders AI message with avatar', () => {
    const msg = createMockMessage({ role: 'assistant', content: 'Hello! How can I help?' });
    render(<ChatMessage message={msg} />);
    expect(screen.getByText('Hello! How can I help?')).toBeInTheDocument();
  });

  it('renders corrections when present', () => {
    const msg = createMockMessage({
      role: 'assistant',
      content: 'Good effort!',
      corrections: [{ original: 'I goed', corrected: 'I went', explanation: 'Irregular verb' }],
    });
    render(<ChatMessage message={msg} />);
    expect(screen.getByText('I goed')).toBeInTheDocument();
    expect(screen.getByText('I went')).toBeInTheDocument();
  });
});

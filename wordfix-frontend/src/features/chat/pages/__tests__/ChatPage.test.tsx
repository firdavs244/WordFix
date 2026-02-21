import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { ChatPage } from '../../pages/ChatPage';

describe('ChatPage', () => {
  it('renders page title', async () => {
    render(<ChatPage />);
    expect(screen.getByText('AI Chat Practice')).toBeInTheDocument();
  });

  it('renders topic selector', () => {
    render(<ChatPage />);
    expect(screen.getByText('Start a Conversation')).toBeInTheDocument();
  });

  it('renders recent conversations section', async () => {
    render(<ChatPage />);
    await waitFor(() => {
      expect(screen.getByText('Recent Conversations')).toBeInTheDocument();
    });
  });
});

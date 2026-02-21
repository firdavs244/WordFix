import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { ChatSessionPage } from '../../pages/ChatSessionPage';

// Mock useParams to return a sessionId
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useParams: () => ({ sessionId: 'chat-1' }), useNavigate: () => vi.fn() };
});

describe('ChatSessionPage', () => {
  it('renders chat session with messages', async () => {
    render(<ChatSessionPage />);
    await waitFor(() => {
      expect(screen.getByText(/travel/i)).toBeInTheDocument();
    });
  });

  it('shows message input area', async () => {
    render(<ChatSessionPage />);
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/type your message/i)).toBeInTheDocument();
    });
  });

  it('displays target words bar', async () => {
    render(<ChatSessionPage />);
    await waitFor(() => {
      expect(screen.getByText('hello')).toBeInTheDocument();
    });
  });
});

import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { ChatHistoryPage } from '../../pages/ChatHistoryPage';

describe('ChatHistoryPage', () => {
  it('renders history title', () => {
    render(<ChatHistoryPage />);
    expect(screen.getByText('Chat History')).toBeInTheDocument();
  });

  it('loads and displays history items', async () => {
    render(<ChatHistoryPage />);
    await waitFor(() => {
      expect(screen.getByText('Travel')).toBeInTheDocument();
      expect(screen.getByText('Food')).toBeInTheDocument();
    });
  });
});

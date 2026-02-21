import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { ConfusingPairsPage } from '../../pages/ConfusingPairsPage';

describe('ConfusingPairsPage', () => {
  it('renders page title', async () => {
    render(<ConfusingPairsPage />);
    expect(await screen.findByText('Confusing Pairs')).toBeInTheDocument();
  });

  it('loads and displays confusing pairs', async () => {
    render(<ConfusingPairsPage />);
    await waitFor(() => {
      expect(screen.getByText('affect')).toBeInTheDocument();
      expect(screen.getByText('effect')).toBeInTheDocument();
    });
  });

  it('shows unresolved pair count', async () => {
    render(<ConfusingPairsPage />);
    await waitFor(() => {
      expect(screen.getByText(/2 pairs to practice/)).toBeInTheDocument();
    });
  });

  it('shows resolved pairs toggle', async () => {
    render(<ConfusingPairsPage />);
    await waitFor(() => {
      expect(screen.getByText(/resolved pairs/i)).toBeInTheDocument();
    });
  });
});

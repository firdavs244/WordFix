import { describe, it, expect } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import AnalyticsPage from '../../pages/AnalyticsPage';

describe('AnalyticsPage', () => {
  it('renders page title', () => {
    render(<AnalyticsPage />);
    expect(screen.getByText('Analytics')).toBeInTheDocument();
  });

  it('loads and displays stats overview', async () => {
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText('50')).toBeInTheDocument(); // total_words
    });
  });

  it('displays weekly chart after load', async () => {
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText('This Week')).toBeInTheDocument();
    });
  });
});

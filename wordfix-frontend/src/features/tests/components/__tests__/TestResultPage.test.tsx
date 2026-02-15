import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import TestResultPage from '../../TestResultPage';

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useParams: () => ({ sessionId: 'ts-1' }) };
});

describe('TestResultPage', () => {
  it('renders loading state initially', () => {
    render(<TestResultPage />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders grade badge after data loads', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByTestId('grade-badge')).toBeInTheDocument();
    });
  });

  it('renders grade letter B for 80% score', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByTestId('grade-letter')).toHaveTextContent('B');
    });
  });

  it('renders score percentage', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByTestId('grade-score')).toHaveTextContent('80%');
    });
  });

  it('renders stats section', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByText('4')).toBeInTheDocument(); // correct
    });
  });

  it('renders Take Another Test link', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByText('Take Another Test')).toBeInTheDocument();
    });
  });

  it('renders Dashboard link', async () => {
    render(<TestResultPage />);
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });
  });
});

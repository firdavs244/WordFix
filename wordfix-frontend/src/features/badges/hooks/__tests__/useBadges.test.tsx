import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { useBadges } from '../useBadges';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}><BrowserRouter>{children}</BrowserRouter></QueryClientProvider>
  );
}

describe('useBadges', () => {
  it('returns badges array', async () => {
    const { result } = renderHook(() => useBadges(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(Array.isArray(result.current.badges)).toBe(true);
  });

  it('returns earned count', async () => {
    const { result } = renderHook(() => useBadges(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(typeof result.current.earnedCount).toBe('number');
    });
  });

  it('returns total count', async () => {
    const { result } = renderHook(() => useBadges(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(typeof result.current.totalCount).toBe('number');
    });
  });
});

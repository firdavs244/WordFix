import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAnalyticsOverview, useWeeklyStats, useDifficultWords } from '../../hooks/useAnalytics';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  );
}

describe('useAnalyticsOverview', () => {
  it('fetches analytics overview', async () => {
    const { result } = renderHook(() => useAnalyticsOverview(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data.total_words).toBe(50);
    expect(result.current.data?.data.overall_accuracy).toBe(80);
  });
});

describe('useWeeklyStats', () => {
  it('fetches weekly stats', async () => {
    const { result } = renderHook(() => useWeeklyStats(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(7);
  });
});

describe('useDifficultWords', () => {
  it('fetches difficult words', async () => {
    const { result } = renderHook(() => useDifficultWords(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(3);
  });
});

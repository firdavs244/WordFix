import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useConfusingPairs, useUnresolvedCount } from '../../hooks/useConfusingPairs';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  );
}

describe('useConfusingPairs', () => {
  it('fetches confusing pairs list', async () => {
    const { result } = renderHook(() => useConfusingPairs(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(3);
    expect(result.current.data?.data[0].word_1.original_word).toBe('affect');
  });
});

describe('useUnresolvedCount', () => {
  it('fetches unresolved count', async () => {
    const { result } = renderHook(() => useUnresolvedCount(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data.count).toBe(2);
  });
});

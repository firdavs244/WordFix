import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import React from 'react';
import { useTestSession, useRecentTests, useCompleteTest } from '../useTests';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 }, mutations: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
}

describe('useTestSession', () => {
  it('fetches test session data', async () => {
    const { result } = renderHook(() => useTestSession('ts-1'), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.session.id).toBe('ts-1');
  });

  it('returns questions with the session', async () => {
    const { result } = renderHook(() => useTestSession('ts-1'), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.questions).toBeDefined();
    expect(result.current.data?.questions.length).toBeGreaterThan(0);
  });
});

describe('useRecentTests', () => {
  it('fetches test history', async () => {
    const { result } = renderHook(() => useRecentTests(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toBeDefined();
    expect(Array.isArray(result.current.data)).toBe(true);
  });

  it('returns test session data', async () => {
    const { result } = renderHook(() => useRecentTests(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.[0]?.score_percentage).toBe(80);
  });
});

describe('useCompleteTest', () => {
  it('completes a test session', async () => {
    const { result } = renderHook(() => useCompleteTest(), { wrapper: createWrapper() });
    await result.current.mutateAsync('ts-1');
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });
});

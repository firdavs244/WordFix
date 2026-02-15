import { describe, it, expect, vi } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import {
  useReviewSummary,
  useReviewHistory,
  useStreak,
  useStartSession,
  useCompleteSession,
  reviewKeys,
} from '../useReview';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 }, mutations: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('useReviewSummary hook', () => {
  it('fetches review summary', async () => {
    const { result } = renderHook(() => useReviewSummary(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data?.words_due).toBe(12);
    expect(result.current.data?.data?.streak_days).toBe(7);
  });
});

describe('useReviewHistory hook', () => {
  it('fetches review history', async () => {
    const { result } = renderHook(() => useReviewHistory(1), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(1);
  });
});

describe('useStreak hook', () => {
  it('fetches streak data', async () => {
    const { result } = renderHook(() => useStreak(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data?.current_streak).toBe(7);
    expect(result.current.data?.data?.longest_streak).toBe(14);
  });
});

describe('useStartSession hook', () => {
  it('starts a review session', async () => {
    const { result } = renderHook(() => useStartSession(), { wrapper: createWrapper() });
    await result.current.mutateAsync('review');
    expect(result.current.isSuccess).toBe(true);
    expect(result.current.data?.data?.id).toBe('ses-1');
  });
});

describe('useCompleteSession hook', () => {
  it('completes a review session', async () => {
    const { result } = renderHook(() => useCompleteSession(), { wrapper: createWrapper() });
    await result.current.mutateAsync('ses-1');
    expect(result.current.isSuccess).toBe(true);
    expect(result.current.data?.data?.is_completed).toBe(true);
  });
});

describe('reviewKeys', () => {
  it('generates correct query keys', () => {
    expect(reviewKeys.all).toEqual(['review']);
    expect(reviewKeys.summary()).toEqual(['review', 'summary']);
    expect(reviewKeys.session('abc')).toEqual(['review', 'sessions', 'abc']);
    expect(reviewKeys.history(2)).toEqual(['review', 'history', 2]);
    expect(reviewKeys.streak()).toEqual(['review', 'streak']);
  });
});

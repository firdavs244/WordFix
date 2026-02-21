import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import { useWords, useWordStats, useCreateWord, useDeleteWord, wordKeys } from '../useWords';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 }, mutations: { retry: false } },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('useWords hook', () => {
  it('fetches words list', async () => {
    const { result } = renderHook(() => useWords(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(3);
  });

  it('fetches words with search filter', async () => {
    const { result } = renderHook(() => useWords({ search: 'hello' }), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(1);
    expect(result.current.data?.data[0].original_word).toBe('hello');
  });

  it('fetches words with difficulty filter', async () => {
    const { result } = renderHook(() => useWords({ difficulty_level: 'hard' }), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data).toHaveLength(1);
  });
});

describe('useWordStats hook', () => {
  it('fetches word stats', async () => {
    const { result } = renderHook(() => useWordStats(), { wrapper: createWrapper() });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.data?.total).toBe(50);
    expect(result.current.data?.data?.mastered).toBe(15);
  });
});

describe('useCreateWord hook', () => {
  it('creates a word successfully', async () => {
    const { result } = renderHook(() => useCreateWord(), { wrapper: createWrapper() });
    await result.current.mutateAsync({ original_word: 'test', difficulty_level: 'easy' });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });
});

describe('useDeleteWord hook', () => {
  it('deletes a word successfully', async () => {
    const { result } = renderHook(() => useDeleteWord(), { wrapper: createWrapper() });
    await result.current.mutateAsync('w1');
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
  });
});

describe('wordKeys', () => {
  it('generates correct query keys', () => {
    expect(wordKeys.all).toEqual(['words']);
    expect(wordKeys.lists()).toEqual(['words', 'list']);
    expect(wordKeys.stats()).toEqual(['words', 'stats']);
    expect(wordKeys.detail('abc')).toEqual(['words', 'detail', 'abc']);
    expect(wordKeys.categories()).toEqual(['words', 'categories']);
  });
});

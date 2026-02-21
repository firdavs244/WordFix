import { describe, it, expect } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useTextImport } from '../../hooks/useTextImport';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  );
}

describe('useTextImport', () => {
  it('initializes with empty state', () => {
    const { result } = renderHook(() => useTextImport(), { wrapper: createWrapper() });
    expect(result.current.text).toBe('');
    expect(result.current.suggestions).toEqual([]);
    expect(result.current.selectedIds.size).toBe(0);
  });

  it('updates text', () => {
    const { result } = renderHook(() => useTextImport(), { wrapper: createWrapper() });
    act(() => result.current.setText('Hello world'));
    expect(result.current.text).toBe('Hello world');
  });

  it('analyzes text and populates suggestions', async () => {
    const { result } = renderHook(() => useTextImport(), { wrapper: createWrapper() });
    act(() => result.current.setText('The adventure was amazing on the journey to the destination.'));
    await act(async () => { await result.current.analyze(); });
    await waitFor(() => expect(result.current.suggestions.length).toBe(3));
    expect(result.current.selectedIds.size).toBe(3);
  });

  it('toggle deselects and reselects', async () => {
    const { result } = renderHook(() => useTextImport(), { wrapper: createWrapper() });
    act(() => result.current.setText('test'));
    await act(async () => { await result.current.analyze(); });
    await waitFor(() => expect(result.current.selectedIds.size).toBe(3));
    act(() => result.current.toggle(0));
    expect(result.current.selectedIds.has(0)).toBe(false);
    act(() => result.current.toggle(0));
    expect(result.current.selectedIds.has(0)).toBe(true);
  });

  it('resets state', async () => {
    const { result } = renderHook(() => useTextImport(), { wrapper: createWrapper() });
    act(() => result.current.setText('test'));
    act(() => result.current.reset());
    expect(result.current.text).toBe('');
    expect(result.current.suggestions).toEqual([]);
  });
});

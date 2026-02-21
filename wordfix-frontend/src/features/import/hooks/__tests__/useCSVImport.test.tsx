import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useCSVImport } from '../../hooks/useCSVImport';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}>{children}</QueryClientProvider>
  );
}

describe('useCSVImport', () => {
  it('initializes with empty state', () => {
    const { result } = renderHook(() => useCSVImport(), { wrapper: createWrapper() });
    expect(result.current.file).toBeNull();
    expect(result.current.previewData).toBeNull();
    expect(result.current.result).toBeNull();
  });

  it('validates a CSV file and gets preview', async () => {
    const { result } = renderHook(() => useCSVImport(), { wrapper: createWrapper() });
    const file = new File(['word,translation\napple,яблоко'], 'words.csv', { type: 'text/csv' });
    await act(async () => { await result.current.validate(file); });
    expect(result.current.file).toBe(file);
    expect(result.current.previewData).not.toBeNull();
    expect(result.current.previewData?.total_rows).toBe(10);
  });

  it('resets state', async () => {
    const { result } = renderHook(() => useCSVImport(), { wrapper: createWrapper() });
    const file = new File(['test'], 'test.csv', { type: 'text/csv' });
    await act(async () => { await result.current.validate(file); });
    act(() => result.current.reset());
    expect(result.current.file).toBeNull();
    expect(result.current.previewData).toBeNull();
  });
});

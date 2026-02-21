import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { useLearningProfileData } from '../useLearningProfile';

function createWrapper() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={qc}><BrowserRouter>{children}</BrowserRouter></QueryClientProvider>
  );
}

describe('useLearningProfileData', () => {
  it('returns profile data', async () => {
    const { result } = renderHook(() => useLearningProfileData(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.profileLoading).toBe(false);
    });

    expect(result.current.profile).toBeDefined();
  });

  it('returns hasAnalyzed flag', async () => {
    const { result } = renderHook(() => useLearningProfileData(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(typeof result.current.hasAnalyzed).toBe('boolean');
    });
  });

  it('provides analyze function', () => {
    const { result } = renderHook(() => useLearningProfileData(), {
      wrapper: createWrapper(),
    });

    expect(typeof result.current.analyze).toBe('function');
    expect(typeof result.current.acceptRecommendation).toBe('function');
  });
});

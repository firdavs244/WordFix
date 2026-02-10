import { useQuery } from '@tanstack/react-query';
import { analyticsApi } from '../api/analyticsApi';

// ─── Query Keys ────────────────────────────────────────────────────────────────

export const analyticsKeys = {
  all: ['analytics'] as const,
  overview: () => [...analyticsKeys.all, 'overview'] as const,
  weekly: () => [...analyticsKeys.all, 'weekly'] as const,
  monthly: () => [...analyticsKeys.all, 'monthly'] as const,
  difficultWords: () => [...analyticsKeys.all, 'difficult-words'] as const,
  wordProgress: () => [...analyticsKeys.all, 'word-progress'] as const,
  calendar: (year?: number, month?: number) =>
    [...analyticsKeys.all, 'calendar', year, month] as const,
};

// ─── Queries ───────────────────────────────────────────────────────────────────

export function useAnalyticsOverview() {
  return useQuery({
    queryKey: analyticsKeys.overview(),
    queryFn: () => analyticsApi.getOverview(),
  });
}

export function useWeeklyStats() {
  return useQuery({
    queryKey: analyticsKeys.weekly(),
    queryFn: () => analyticsApi.getWeekly(),
  });
}

export function useMonthlyStats() {
  return useQuery({
    queryKey: analyticsKeys.monthly(),
    queryFn: () => analyticsApi.getMonthly(),
  });
}

export function useDifficultWords() {
  return useQuery({
    queryKey: analyticsKeys.difficultWords(),
    queryFn: () => analyticsApi.getDifficultWords(),
  });
}

export function useWordProgress() {
  return useQuery({
    queryKey: analyticsKeys.wordProgress(),
    queryFn: () => analyticsApi.getWordProgress(),
  });
}

export function useStudyCalendar(year?: number, month?: number) {
  return useQuery({
    queryKey: analyticsKeys.calendar(year, month),
    queryFn: () => analyticsApi.getCalendar(year, month),
  });
}

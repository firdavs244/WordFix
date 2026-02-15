import { useWordStats, useWords } from '@/features/words/hooks/useWords';
import { useUserProgress, useXPHistory } from '@/features/progress/hooks/useProgress';
import { useDailyChallenges } from '@/features/challenges/hooks/useChallenges';
import { useReviewSummary, useStreak, useDailyProgress } from '@/features/review/hooks/useReview';
import { useDomainCoverage, useMistakePatterns, useWordRecommendations } from '@/features/learning/hooks/useLearning';

export function useDashboardData() {
  const stats = useWordStats();
  const recentWords = useWords({ page: 1, page_size: 5, ordering: '-created_at' });
  const progress = useUserProgress();
  const challenges = useDailyChallenges();
  const summary = useReviewSummary();
  const streak = useStreak();
  const daily = useDailyProgress();
  const xpHistory = useXPHistory(7);
  const domains = useDomainCoverage();
  const mistakes = useMistakePatterns();
  const recommendations = useWordRecommendations();

  return {
    stats: stats.data?.data,
    recentWords: recentWords.data?.data ?? [],
    progress: progress.data?.data,
    challenges: challenges.data?.data,
    summary: summary.data?.data,
    streak: streak.data?.data,
    daily: daily.data?.data,
    xpHistory: xpHistory.data?.data ?? [],
    domains: domains.data?.data,
    mistakes: mistakes.data?.data ?? [],
    recommendations: recommendations.data?.data ?? [],
    isLoading: stats.isLoading || recentWords.isLoading || progress.isLoading,
  };
}

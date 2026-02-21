import { useMemo } from 'react';
import { useAllBadges, useUserBadges } from '@/features/progress/hooks/useProgress';
import type { BadgeData } from '@/types';

export function useBadges() {
  const allBadgesQuery = useAllBadges();
  const userBadgesQuery = useUserBadges();

  const badges = useMemo<BadgeData[]>(() => {
    const all = allBadgesQuery.data?.data ?? [];
    const earned = userBadgesQuery.data?.data?.badges ?? [];
    const earnedMap = new Map(earned.map((b) => [b.id, b]));

    return all.map((badge) => {
      const userBadge = earnedMap.get(badge.id);
      if (userBadge) {
        return { ...badge, is_earned: true, earned_at: userBadge.earned_at };
      }
      return { ...badge, is_earned: false, earned_at: null };
    });
  }, [allBadgesQuery.data, userBadgesQuery.data]);

  const earnedCount = badges.filter((b) => b.is_earned).length;
  const totalCount = badges.length;
  const isLoading = allBadgesQuery.isLoading || userBadgesQuery.isLoading;

  return { badges, isLoading, earnedCount, totalCount };
}

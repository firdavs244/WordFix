import { useMemo } from 'react';
import { useAllBadges, useUserBadges } from '@/features/progress/hooks/useProgress';
import type { BadgeData } from '@/types';

export function useBadges() {
  const allBadgesQuery = useAllBadges();
  const userBadgesQuery = useUserBadges();

  const badges = useMemo<BadgeData[]>(() => {
    const all = allBadgesQuery.data?.data ?? [];
    const earned = userBadgesQuery.data?.data?.badges ?? [];
    // Only include badges that are actually earned (is_earned === true)
    const earnedOnly = earned.filter((b: BadgeData) => b.is_earned);
    const earnedMap = new Map(earnedOnly.map((b: BadgeData) => [b.id, b]));

    return all.map((badge: BadgeData) => {
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

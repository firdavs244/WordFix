import type { BadgeData } from '@/types';
import BadgeCardEarned from './BadgeCardEarned';
import BadgeCardLocked from './BadgeCardLocked';

interface BadgeCardProps {
  badge: BadgeData;
}

export default function BadgeCard({ badge }: BadgeCardProps) {
  if (badge.is_earned) return <BadgeCardEarned badge={badge} />;
  return <BadgeCardLocked badge={badge} />;
}

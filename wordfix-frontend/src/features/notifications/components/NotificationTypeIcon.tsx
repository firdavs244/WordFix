import {
  Bell,
  Trophy,
  Flame,
  Star,
  Target,
  BookOpen,
  BarChart3,
} from 'lucide-react';
import type { NotificationType } from '@/types/core';

const iconMap: Record<NotificationType, React.ComponentType<{ className?: string }>> = {
  review_reminder: BookOpen,
  streak_warning: Flame,
  badge_earned: Trophy,
  level_up: Star,
  daily_goal_complete: Target,
  word_mastered: Star,
  weekly_report: BarChart3,
};

const colorMap: Record<NotificationType, string> = {
  review_reminder: 'text-blue-400',
  streak_warning: 'text-orange-400',
  badge_earned: 'text-yellow-400',
  level_up: 'text-purple-400',
  daily_goal_complete: 'text-emerald-400',
  word_mastered: 'text-cyan-400',
  weekly_report: 'text-indigo-400',
};

interface Props {
  type: NotificationType;
  className?: string;
}

export function NotificationTypeIcon({ type, className = '' }: Props) {
  const Icon = iconMap[type] ?? Bell;
  const color = colorMap[type] ?? 'text-muted-foreground';

  return (
    <div
      className={`flex h-9 w-9 items-center justify-center rounded-full bg-muted/60 ${color} ${className}`}
      aria-hidden="true"
    >
      <Icon className="h-4 w-4" />
    </div>
  );
}

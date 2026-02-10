import { motion } from 'framer-motion';
import {
  BookOpen,
  Plus,
  Star,
  Gamepad2,
  ClipboardCheck,
  Flame,
  MessageSquare,
  Trophy,
  CheckCircle2,
} from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import type { Challenge } from '../types';

interface ChallengeCardProps {
  challenge: Challenge;
}

const iconMap: Record<string, React.FC<{ className?: string }>> = {
  review_words: BookOpen,
  add_words: Plus,
  perfect_review: Star,
  play_game: Gamepad2,
  complete_test: ClipboardCheck,
  combo_streak: Flame,
  chat_practice: MessageSquare,
  master_word: Trophy,
};

export function ChallengeCard({ challenge }: ChallengeCardProps) {
  const Icon = iconMap[challenge.icon] ?? Star;
  const progressPct = challenge.target > 0
    ? Math.min((challenge.current / challenge.target) * 100, 100)
    : 0;

  return (
    <motion.div
      className={cn(
        'flex items-center gap-3 rounded-lg p-3 transition-colors',
        challenge.completed
          ? 'bg-green-500/5 dark:bg-green-500/10'
          : 'bg-muted/50',
      )}
      layout
    >
      {/* Icon */}
      <div
        className={cn(
          'flex h-9 w-9 shrink-0 items-center justify-center rounded-lg',
          challenge.completed
            ? 'bg-green-500/10'
            : 'bg-primary/10',
        )}
      >
        {challenge.completed ? (
          <CheckCircle2 className="h-5 w-5 text-green-500" />
        ) : (
          <Icon className="h-5 w-5 text-primary" />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <p
            className={cn(
              'text-sm font-medium',
              challenge.completed && 'text-muted-foreground',
            )}
          >
            {challenge.title}
          </p>
          <span className="text-xs font-medium text-muted-foreground">
            {challenge.current}/{challenge.target}
          </span>
        </div>
        {!challenge.completed && (
          <div className="mt-1.5" role="progressbar" aria-valuenow={challenge.current} aria-valuemax={challenge.target}>
            <Progress value={progressPct} className="h-1.5" />
          </div>
        )}
        <p className={cn(
          'mt-1 text-xs',
          challenge.completed ? 'text-green-600 dark:text-green-400' : 'text-amber-500',
        )}>
          {challenge.completed ? 'Completed!' : `+${challenge.xp_reward} XP`}
        </p>
      </div>
    </motion.div>
  );
}

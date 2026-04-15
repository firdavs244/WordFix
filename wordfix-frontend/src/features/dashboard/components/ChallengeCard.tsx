import { motion } from 'framer-motion';
import {
  BookOpen, Plus, Star, Gamepad2, ClipboardCheck,
  Flame, MessageSquare, Trophy, CheckCircle2, Zap,
} from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import type { Challenge } from '@/features/challenges/types';

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  review_words: BookOpen, add_words: Plus, perfect_review: Star,
  play_game: Gamepad2, complete_test: ClipboardCheck, combo_streak: Flame,
  chat_practice: MessageSquare, master_word: Trophy,
};

export default function ChallengeCard({ challenge }: { challenge: Challenge }) {
  const Icon = ICON_MAP[challenge.type] ?? Star;
  const progress = Math.min((challenge.current / challenge.target) * 100, 100);

  if (challenge.completed) {
    return (
      <motion.div
        variants={staggerItem}
        className="flex items-center gap-3 rounded-xl bg-success/[0.04] p-3"
      >
        <div className="flex h-[34px] w-[34px] items-center justify-center rounded-lg bg-success/10">
          <CheckCircle2 className="h-4 w-4 text-success" />
        </div>
        <span className="flex-1 text-sm font-medium text-success/70 line-through">
          {challenge.title}
        </span>
        <span className="text-[10px] font-medium text-success">Done</span>
      </motion.div>
    );
  }

  return (
    <motion.div
      variants={staggerItem}
      className="flex items-center gap-3 rounded-xl p-3 transition-all duration-200 hover:bg-muted/30"
    >
      <div className="flex h-[34px] w-[34px] items-center justify-center rounded-lg bg-muted/50">
        <Icon className="h-4 w-4 text-muted-foreground" />
      </div>
      <span className="flex-1 text-sm font-medium">{challenge.title}</span>
      <div className="flex items-center gap-2">
        <div className="h-1.5 w-20 overflow-hidden rounded-full bg-muted">
          <motion.div
            className="h-full rounded-full bg-primary"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
        <span className="text-[10px] text-muted-foreground">
          {challenge.current}/{challenge.target}
        </span>
      </div>
      <span className="flex items-center gap-0.5 text-[11px] font-semibold text-accent">
        <Zap className="h-[10px] w-[10px]" />+{challenge.xp_reward} XP
      </span>
    </motion.div>
  );
}

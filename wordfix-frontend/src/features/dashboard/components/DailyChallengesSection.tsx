import { motion, AnimatePresence } from 'framer-motion';
import { ClipboardList } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { Skeleton } from '@/components/ui/skeleton';
import { useDailyChallenges } from '@/features/challenges/hooks/useChallenges';
import ChallengeCard from './ChallengeCard';
import ChallengeBonusButton from './ChallengeBonusButton';

export default function DailyChallengesSection() {
  const { data, isLoading } = useDailyChallenges();
  const challenges = data?.data;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card shadow-card p-5">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <Skeleton key={i} className="h-14 rounded-xl" />)}
        </div>
      </div>
    );
  }

  const allDone = challenges?.all_completed ?? false;
  const done = challenges?.challenges.filter((c) => c.completed).length ?? 0;
  const total = challenges?.challenges.length ?? 0;

  return (
    <div className="overflow-hidden rounded-2xl border border-border/50 bg-card shadow-card">
      {/* Gradient stripe */}
      <div className={`h-1 w-full bg-gradient-to-r from-primary via-secondary to-accent ${
        allDone ? 'animate-[gradient-shift_3s_linear_infinite] bg-[length:200%_100%]' : ''
      }`} />

      {/* Header */}
      <div className="flex items-center justify-between px-5 lg:px-6 pt-5">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10">
            <ClipboardList className="h-[18px] w-[18px] text-primary" />
          </div>
          <h3 className="text-base font-heading font-semibold">Daily Challenges</h3>
        </div>
        <AnimatePresence mode="wait">
          {allDone ? (
            <motion.span
              key="done"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="rounded-full bg-success/10 px-3 py-1 text-xs font-semibold text-success"
            >
              ✓ All Done
            </motion.span>
          ) : (
            <motion.span
              key="progress"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="rounded-full bg-muted px-3 py-1 text-xs font-medium text-muted-foreground"
            >
              {done}/{total}
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Challenge list */}
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-1.5 px-5 lg:px-6 py-4"
      >
        {challenges?.challenges.map((challenge, i) => (
          <ChallengeCard key={`${challenge.type}-${i}`} challenge={challenge} />
        ))}
      </motion.div>

      {/* Bonus section */}
      {allDone && (
        <>
          <div className="mx-5 border-t border-border/30" />
          <div className="px-5 pb-5 pt-4">
            <ChallengeBonusButton
              allCompleted={allDone}
              bonusClaimed={challenges?.bonus_claimed ?? false}
            />
          </div>
        </>
      )}
    </div>
  );
}

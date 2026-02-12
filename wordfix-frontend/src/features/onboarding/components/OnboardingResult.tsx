import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, PartyPopper, Sparkles, Trophy } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { LevelIndicator, LevelScale } from '@/features/onboarding/components/LevelIndicator';
import type { OnboardingResult as ResultType } from '@/features/onboarding/types';

interface OnboardingResultProps {
  result: ResultType;
  onContinue: () => void;
}

export function OnboardingResult({ result, onContinue }: OnboardingResultProps) {
  const [displayXP, setDisplayXP] = useState(0);
  const isHighLevel = ['B2', 'C1', 'C2'].includes(result.determined_level);

  const xpEarned = result.xp_earned ?? 0;

  // XP count-up animation
  useEffect(() => {
    if (xpEarned <= 0) return;
    const duration = 1500;
    const steps = 30;
    const increment = xpEarned / steps;
    let current = 0;
    const interval = setInterval(() => {
      current += increment;
      if (current >= xpEarned) {
        setDisplayXP(xpEarned);
        clearInterval(interval);
      } else {
        setDisplayXP(Math.round(current));
      }
    }, duration / steps);
    return () => clearInterval(interval);
  }, [xpEarned]);

  // Confetti for B2+ levels
  useEffect(() => {
    if (!isHighLevel) return;
    const timer = setTimeout(async () => {
      try {
        const confetti = (await import('canvas-confetti')).default;
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
        });
      } catch {
        // canvas-confetti not available — skip
      }
    }, 600);
    return () => clearTimeout(timer);
  }, [isHighLevel]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: 'spring', stiffness: 200, damping: 20 }}
      className="flex flex-col items-center gap-8 text-center"
    >
      {/* Celebration icon */}
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: 'spring', stiffness: 300, damping: 15 }}
        className="relative"
      >
        {isHighLevel ? (
          <Trophy className="h-16 w-16 text-yellow-500" />
        ) : (
          <PartyPopper className="h-16 w-16 text-primary" />
        )}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.2, 1] }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="absolute -right-2 -top-2"
        >
          <Sparkles className="h-6 w-6 text-yellow-400" />
        </motion.div>
      </motion.div>

      {/* Level result */}
      <div className="space-y-4">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-2xl font-bold md:text-3xl"
        >
          Your English Level
        </motion.h2>

        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: 'spring', stiffness: 200, damping: 15 }}
        >
          <LevelIndicator level={result.determined_level} size="lg" />
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          <LevelScale currentLevel={result.determined_level} />
        </motion.div>
      </div>

      {/* Stats */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="flex items-center gap-8"
      >
        <div className="text-center">
          <p className="text-2xl font-bold text-primary">{result.total_correct}</p>
          <p className="text-xs text-muted-foreground">Correct</p>
        </div>
        <div className="h-8 w-px bg-border" />
        <div className="text-center">
          <p className="text-2xl font-bold text-foreground">{result.total_questions}</p>
          <p className="text-xs text-muted-foreground">Questions</p>
        </div>
        <div className="h-8 w-px bg-border" />
        <div className="text-center">
          <p className="text-2xl font-bold text-yellow-500">+{displayXP}</p>
          <p className="text-xs text-muted-foreground">XP Earned</p>
        </div>
      </motion.div>

      {/* Message */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.0 }}
        className="max-w-md text-muted-foreground"
      >
        {result.message}
      </motion.p>

      {/* Continue button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2 }}
      >
        <Button size="lg" className="gap-2" onClick={onContinue}>
          Start Learning
          <ArrowRight className="h-4 w-4" />
        </Button>
      </motion.div>
    </motion.div>
  );
}

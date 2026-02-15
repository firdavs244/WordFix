import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { bounceIn } from '@/lib/motion';
import { useConfetti } from '@/components/shared';
import { LevelBadge } from './LevelBadge';
import type { OnboardingResult as ResultType } from '../types';

const descriptions: Record<string, string> = {
  A1: 'Beginner — You\'re starting your journey!',
  A2: 'Elementary — You know the basics!',
  B1: 'Intermediate — You can handle everyday situations!',
  B2: 'Upper Intermediate — You communicate with confidence!',
  C1: 'Advanced — You express yourself fluently!',
  C2: 'Mastery — You\'re nearly native-level!',
};

interface Props {
  result: ResultType;
  onContinue: () => void;
}

export function OnboardingResultScreen({ result, onContinue }: Props) {
  const { fireConfetti } = useConfetti();

  useEffect(() => {
    const t = setTimeout(() => fireConfetti({ particleCount: 120 }), 300);
    return () => clearTimeout(t);
  }, [fireConfetti]);

  const level = result.determined_level;

  return (
    <motion.div variants={bounceIn} initial="initial" animate="animate" className="text-center">
      <motion.span
        className="inline-block text-5xl"
        animate={{ y: [0, -8, 0] }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        🎉
      </motion.span>

      <h2 className="mt-2 font-heading text-xl font-bold">Assessment Complete!</h2>

      <div className="my-8 flex justify-center">
        <LevelBadge level={level} size="lg" />
      </div>

      <p className="mx-auto max-w-sm text-sm leading-relaxed text-muted-foreground">
        {descriptions[level] || result.message}
      </p>

      <motion.button
        onClick={onContinue}
        className="mt-8 inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-secondary font-semibold text-white shadow-lg transition-all hover:shadow-xl"
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        Start Learning <Sparkles className="h-4 w-4" />
      </motion.button>
    </motion.div>
  );
}

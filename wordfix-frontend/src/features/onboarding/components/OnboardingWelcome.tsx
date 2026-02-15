import { motion } from 'framer-motion';
import { Brain, ArrowRight } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import { Logo } from '@/components/shared';
import { OnboardingStats } from './OnboardingStats';

interface Props {
  onStart: () => void;
  onSkip: () => void;
  isLoading: boolean;
  totalQuestions: number;
}

export function OnboardingWelcome({ onStart, onSkip, isLoading, totalQuestions }: Props) {
  return (
    <motion.div variants={fadeInUp} initial="initial" animate="animate" exit={{ opacity: 0, y: -20 }} className="text-center">
      <Logo size="lg" className="mx-auto mb-8" />

      <div className="mx-auto flex h-20 w-20 animate-float items-center justify-center rounded-3xl bg-gradient-to-br from-primary/15 to-secondary/10 shadow-glow-primary ring-4 ring-primary/5">
        <Brain className="h-10 w-10 text-primary" />
      </div>

      <h1 className="mt-6 font-heading text-2xl font-bold">Welcome to WordFix!</h1>
      <p className="mx-auto mt-2 max-w-sm text-sm leading-relaxed text-muted-foreground">
        Keling, ingliz tilingiz darajasini aniqlaylik. Bu qisqa test 3-5 daqiqa davom etadi va o'rganish tajribangizni moslashtiradi.
      </p>

      <OnboardingStats totalQuestions={totalQuestions} />

      <motion.button
        onClick={onStart}
        disabled={isLoading}
        className="mt-8 inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 font-semibold text-white shadow-lg shadow-primary/20 transition-all hover:shadow-xl disabled:opacity-60"
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        {isLoading ? 'Loading...' : <>Start Assessment <ArrowRight className="h-4 w-4" /></>}
      </motion.button>

      <button onClick={onSkip} className="mt-4 text-sm text-muted-foreground/60 underline underline-offset-4 transition hover:text-muted-foreground">
        Skip for now →
      </button>
    </motion.div>
  );
}

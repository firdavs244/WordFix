import { motion, AnimatePresence } from 'framer-motion';
import { Lightbulb, Loader2 } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import type { HintResponse } from '../../types/immersive';

interface HintPanelProps {
  hint: HintResponse | null;
  hintsRemaining: number;
  onRequestHint: () => void;
  isLoading: boolean;
}

const PENALTY_MAP: Record<number, number> = { 1: 5, 2: 10, 3: 15 };

export default function HintPanel({ hint, hintsRemaining, onRequestHint, isLoading }: HintPanelProps) {
  const nextPenalty = PENALTY_MAP[4 - hintsRemaining] || 15;

  return (
    <div role="complementary" aria-label="Hint panel" className="space-y-2">
      {/* Request button */}
      {!hint && (
        <button
          onClick={onRequestHint}
          disabled={hintsRemaining <= 0 || isLoading}
          aria-label={hintsRemaining > 0 ? `Request hint (${hintsRemaining} remaining)` : 'No hints remaining'}
          className="flex items-center gap-2 rounded-lg bg-amber-50 px-3 py-2 text-sm font-medium text-amber-700 transition-colors hover:bg-amber-100 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-amber-900/20 dark:text-amber-300 dark:hover:bg-amber-900/30"
        >
          {isLoading ? (
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
          ) : (
            <Lightbulb className="h-4 w-4" aria-hidden="true" />
          )}
          <span>Get Hint</span>
          <span className="ml-auto rounded-full bg-amber-200/60 px-1.5 py-0.5 text-xs dark:bg-amber-800/40">
            {hintsRemaining}/3
          </span>
        </button>
      )}

      {/* Penalty warning */}
      {!hint && hintsRemaining > 0 && hintsRemaining < 3 && (
        <p className="text-xs text-amber-600/70 dark:text-amber-400/60">
          Score penalty: -{nextPenalty}%
        </p>
      )}

      {/* Hint display */}
      <AnimatePresence>
        {hint && (
          <motion.div
            {...fadeInUp}
            exit={{ opacity: 0, y: -8, transition: { duration: 0.15 } }}
            className="rounded-xl border border-amber-200/60 bg-amber-50/80 p-3 dark:border-amber-800/30 dark:bg-amber-900/20"
          >
            <div className="mb-1.5 flex items-center gap-2">
              <Lightbulb className="h-4 w-4 text-amber-500" aria-hidden="true" />
              <span className="text-xs font-semibold uppercase tracking-wide text-amber-600 dark:text-amber-400">
                Hint Level {hint.level}
              </span>
              <span className="ml-auto text-xs text-amber-500/70">-{hint.score_penalty}%</span>
            </div>
            <p className="text-sm text-gray-700 dark:text-gray-200">{hint.hint}</p>
            {hint.hint_uz && (
              <p className="mt-1 text-xs italic text-gray-400">{hint.hint_uz}</p>
            )}
            <div className="mt-2 flex items-center justify-between">
              <span className="text-xs text-gray-400">{hint.hints_remaining} hints remaining</span>
              {hint.hints_remaining > 0 && (
                <button
                  onClick={onRequestHint}
                  disabled={isLoading}
                  className="text-xs font-medium text-amber-600 hover:text-amber-700 dark:text-amber-400"
                >
                  {isLoading ? 'Loading...' : 'Need more help?'}
                </button>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

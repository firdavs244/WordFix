import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { scaleIn } from '@/lib/motion';
import type { GrammarError, VocabFeedback } from '../../types/immersive';

interface ErrorHighlightProps {
  grammarErrors: GrammarError[];
  vocabularyFeedback?: VocabFeedback[];
}

export default function ErrorHighlight({ grammarErrors, vocabularyFeedback = [] }: ErrorHighlightProps) {
  const [expandedIdx, setExpandedIdx] = useState<number | null>(null);

  if (grammarErrors.length === 0 && vocabularyFeedback.length === 0) return null;

  return (
    <motion.div {...scaleIn} className="mt-2 space-y-1.5" role="alert" aria-label="Language corrections">
      {grammarErrors.map((error, i) => (
        <div key={`g-${i}`} className="rounded-lg border border-red-200/60 bg-red-50/50 p-2 dark:border-red-800/30 dark:bg-red-900/10">
          <button
            onClick={() => setExpandedIdx(expandedIdx === i ? null : i)}
            className="flex w-full items-center gap-2 text-left text-sm"
            aria-expanded={expandedIdx === i}
            aria-controls={`error-detail-${i}`}
          >
            <AlertCircle className="h-3.5 w-3.5 shrink-0 text-red-500" aria-hidden="true" />
            <span className="flex-1">
              <span className="text-red-500 line-through">{error.original}</span>
              <span className="mx-1 text-gray-400">→</span>
              <span className="font-medium text-emerald-600 dark:text-emerald-400">{error.corrected}</span>
            </span>
            {expandedIdx === i ? (
              <ChevronUp className="h-3.5 w-3.5 text-gray-400" />
            ) : (
              <ChevronDown className="h-3.5 w-3.5 text-gray-400" />
            )}
          </button>

          <AnimatePresence>
            {expandedIdx === i && (
              <motion.div
                id={`error-detail-${i}`}
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1, transition: { duration: 0.2 } }}
                exit={{ height: 0, opacity: 0, transition: { duration: 0.15 } }}
                className="overflow-hidden"
              >
                <div className="mt-1.5 border-t border-red-200/40 pt-1.5 text-xs dark:border-red-800/20">
                  <p className="text-gray-600 dark:text-gray-300">{error.explanation}</p>
                  <p className="mt-0.5 italic text-gray-400">{error.explanation_uz}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      ))}

      {vocabularyFeedback.map((fb, i) => (
        <div key={`v-${i}`} className="rounded-lg border border-blue-200/60 bg-blue-50/50 p-2 dark:border-blue-800/30 dark:bg-blue-900/10">
          <div className="flex items-center gap-2 text-sm">
            <span className="font-medium text-blue-600 dark:text-blue-400">{fb.word}</span>
            <span className="text-gray-500 dark:text-gray-400">—</span>
            <span className="text-gray-600 dark:text-gray-300">{fb.feedback}</span>
          </div>
          {fb.feedback_uz && (
            <p className="mt-0.5 text-xs italic text-gray-400">{fb.feedback_uz}</p>
          )}
        </div>
      ))}
    </motion.div>
  );
}

/**
 * Immersive Game — Session result page.
 * Sprint 15 — framer-motion animations, animated score counter, ARIA, modern design.
 */

import { useEffect, useState } from 'react';
import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { Trophy, Clock, MessageCircle, Lightbulb, ArrowLeft, RotateCcw } from 'lucide-react';
import { pageTransition, bounceIn, staggerContainer, staggerItem, progressFill } from '@/lib/motion';
import type { SessionCompleteResult } from './types/immersive';

interface Props {
  result: SessionCompleteResult;
  onBack: () => void;
}

function AnimatedCounter({ value }: { value: number }) {
  const [display, setDisplay] = useState(0);
  const motionVal = useMotionValue(0);
  const rounded = useTransform(motionVal, (v) => Math.round(v));

  useEffect(() => {
    const unsub = rounded.on('change', (v) => setDisplay(v));
    const controls = animate(motionVal, value, { duration: 1.2, ease: 'easeOut' });
    return () => { unsub(); controls.stop(); };
  }, [value, motionVal, rounded]);

  return <span>{display}</span>;
}

export function ImmersiveResultPage({ result, onBack }: Props) {
  const scores = [
    { label: 'Fluency', value: result.fluency_score, color: 'bg-blue-500' },
    { label: 'Accuracy', value: result.accuracy_score, color: 'bg-green-500' },
    { label: 'Vocabulary', value: result.vocabulary_score, color: 'bg-purple-500' },
    { label: 'Task Completion', value: result.task_completion_score, color: 'bg-orange-500' },
  ];

  const headerEmoji = result.total_score >= 80 ? '🌟' : result.total_score >= 50 ? '👏' : '💪';
  const headerMessage = result.total_score >= 80
    ? 'Excellent conversation! Keep it up!'
    : result.total_score >= 50
      ? 'Good effort! Practice makes perfect.'
      : 'Nice try! Keep practicing to improve.';

  return (
    <motion.div {...pageTransition} className="mx-auto max-w-2xl space-y-6 py-8 px-4">
      {/* Header */}
      <motion.div {...bounceIn} className="text-center">
        <div className="mb-4 text-6xl" aria-hidden="true">{headerEmoji}</div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Session Complete!</h1>
        <p className="mt-2 text-gray-500 dark:text-gray-400">{headerMessage}</p>
      </motion.div>

      {/* Total Score */}
      <motion.div
        {...bounceIn}
        className="rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-600 p-6 text-center text-white shadow-lg"
      >
        <p className="text-sm font-medium opacity-80">Total Score</p>
        <p className="text-5xl font-bold" aria-label={`Total score: ${result.total_score}`}>
          <AnimatedCounter value={result.total_score} />
        </p>
        <div className="mt-3 flex items-center justify-center gap-4 text-sm opacity-80">
          <span className="flex items-center gap-1">
            <MessageCircle className="h-3.5 w-3.5" aria-hidden="true" />
            {result.turn_count} turns
          </span>
          <span className="flex items-center gap-1">
            <Clock className="h-3.5 w-3.5" aria-hidden="true" />
            {Math.floor(result.duration_seconds / 60)}:{(result.duration_seconds % 60).toString().padStart(2, '0')}
          </span>
          <span className="flex items-center gap-1">
            <Lightbulb className="h-3.5 w-3.5" aria-hidden="true" />
            {result.hints_used} hints
          </span>
        </div>
      </motion.div>

      {/* Score Breakdown */}
      <motion.div
        {...staggerContainer}
        initial="initial"
        animate="animate"
        className="rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800"
      >
        <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100">Score Breakdown</h2>
        <div className="space-y-4">
          {scores.map((score, i) => (
            <motion.div key={score.label} variants={staggerItem}>
              <div className="mb-1.5 flex items-center justify-between">
                <span className="text-sm text-gray-600 dark:text-gray-400">{score.label}</span>
                <span className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                  {score.value.toFixed(1)}%
                </span>
              </div>
              <div
                className="h-2.5 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700"
                role="progressbar"
                aria-valuenow={Math.round(score.value)}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={`${score.label}: ${score.value.toFixed(1)}%`}
              >
                <motion.div
                  className={`h-full rounded-full ${score.color}`}
                  {...progressFill(Math.min(score.value, 100), 0.2 + i * 0.1)}
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* XP & Badges */}
      <motion.div {...staggerContainer} initial="initial" animate="animate" className="flex gap-4">
        <motion.div
          variants={staggerItem}
          className="flex-1 rounded-xl border border-gray-200 bg-white p-4 text-center dark:border-gray-700 dark:bg-gray-800"
        >
          <Trophy className="mx-auto mb-1 h-5 w-5 text-indigo-500" aria-hidden="true" />
          <p className="text-2xl font-bold text-indigo-500">+{result.xp_earned}</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">XP Earned</p>
        </motion.div>
        {result.badges_earned.length > 0 && (
          <motion.div
            variants={staggerItem}
            className="flex-1 rounded-xl border border-gray-200 bg-white p-4 text-center dark:border-gray-700 dark:bg-gray-800"
          >
            <div className="text-2xl" aria-hidden="true">{result.badges_earned[0].icon}</div>
            <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{result.badges_earned[0].name}</p>
          </motion.div>
        )}
      </motion.div>

      {/* Actions */}
      <motion.div variants={staggerItem} className="flex gap-3">
        <button
          onClick={onBack}
          aria-label="Back to scenarios"
          className="flex flex-1 items-center justify-center gap-2 rounded-lg border border-gray-300 px-4 py-3 font-medium text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
        >
          <ArrowLeft className="h-4 w-4" />
          Back
        </button>
        <button
          onClick={onBack}
          aria-label="Play again"
          className="flex flex-1 items-center justify-center gap-2 rounded-lg bg-indigo-500 px-4 py-3 font-medium text-white hover:bg-indigo-600"
        >
          <RotateCcw className="h-4 w-4" />
          Play Again
        </button>
      </motion.div>
    </motion.div>
  );
}

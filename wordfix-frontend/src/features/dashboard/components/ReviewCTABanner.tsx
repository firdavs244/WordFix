import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Brain, ArrowRight } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import { useReviewSummary } from '@/features/review/hooks/useReview';

export default function ReviewCTABanner() {
  const { data } = useReviewSummary();
  const wordsDue = data?.data?.words_due ?? 0;

  return (
    <AnimatePresence>
      {wordsDue > 0 && (
        <motion.div
          variants={fadeInUp}
          initial="initial"
          animate="animate"
          exit={{ opacity: 0, y: -10 }}
          className="relative overflow-hidden rounded-2xl border border-primary/15"
          style={{
            background: 'linear-gradient(to right, hsl(var(--primary) / 0.06), hsl(var(--primary) / 0.03), hsl(var(--secondary) / 0.05))',
          }}
        >
          {/* Decorative large icon */}
          <Brain className="pointer-events-none absolute -right-4 top-1/2 h-[120px] w-[120px] -translate-y-1/2 rotate-12 text-primary/[0.04]" />

          <div className="relative z-10 flex items-center gap-4 lg:gap-6 p-5 lg:p-6">
            {/* Brain icon container */}
            <motion.div
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/10"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
            >
              <Brain className="h-6 w-6 text-primary" />
            </motion.div>

            {/* Text */}
            <div className="flex-1">
              <p className="text-base font-heading font-semibold">Time to review!</p>
              <p className="text-sm text-muted-foreground">
                You have {wordsDue} words waiting
              </p>
              {wordsDue > 20 && (
                <p className="mt-0.5 text-xs text-destructive/60">Don't let them pile up!</p>
              )}
            </div>

            {/* CTA */}
            <Link
              to="/review"
              className="inline-flex items-center gap-2 rounded-xl bg-primary px-5 py-2.5 text-sm font-medium text-white shadow-md transition-all hover:scale-[1.02] hover:shadow-[0_0_16px_hsl(var(--primary)/0.3)]"
            >
              Start Review
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

import { useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { bounceIn, fadeIn } from '@/lib/motion';
import { AnimatedCounter, useConfetti } from '@/components/shared';
import { Button } from '@/components/ui/button';

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function ChallengeBonusModal({ open, onClose }: Props) {
  const { fireConfetti } = useConfetti();

  useEffect(() => {
    if (open) {
      fireConfetti({ particleCount: 150, spread: 80 });
      document.body.style.overflow = 'hidden';
    }
    return () => { document.body.style.overflow = ''; };
  }, [open, fireConfetti]);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); },
    [onClose],
  );

  useEffect(() => {
    if (open) {
      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
    }
  }, [open, handleKeyDown]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          variants={fadeIn}
          initial="initial"
          animate="animate"
          exit="initial"
          className="fixed inset-0 z-50 flex items-start justify-center bg-black/60 backdrop-blur-md"
          onClick={onClose}
        >
          <motion.div
            variants={bounceIn}
            initial="initial"
            animate="animate"
            className="mx-4 mt-[25vh] w-full max-w-sm rounded-3xl border border-border/30 bg-card p-8 text-center shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <motion.span
              className="inline-block text-5xl"
              animate={{ y: [0, -10, 0, -5, 0] }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              🎉
            </motion.span>

            <h2 className="mt-4 text-xl font-heading font-bold">Bonus Claimed!</h2>

            <div className="relative mt-2">
              <p className="text-3xl font-heading font-bold text-accent">
                +<AnimatedCounter value={50} /> XP
              </p>
              {/* Sparkle dots */}
              {[0, 1, 2, 3].map((i) => (
                <span
                  key={i}
                  className="absolute h-1 w-1 rounded-full bg-accent animate-ping"
                  style={{
                    top: `${20 + Math.sin(i * 1.57) * 30}%`,
                    left: `${35 + Math.cos(i * 1.57) * 30}%`,
                    animationDelay: `${i * 0.2}s`,
                    animationDuration: '1.5s',
                  }}
                />
              ))}
            </div>

            <p className="mt-3 text-sm text-muted-foreground">
              Keep completing daily challenges to earn more!
            </p>

            <Button onClick={onClose} className="mt-6 w-full rounded-xl">
              Continue
            </Button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

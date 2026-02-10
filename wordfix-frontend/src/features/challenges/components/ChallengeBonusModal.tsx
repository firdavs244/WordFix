import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useEffect } from 'react';
import confetti from 'canvas-confetti';

interface ChallengeBonusModalProps {
  isOpen: boolean;
  onClose: () => void;
  xpEarned?: number;
}

export function ChallengeBonusModal({ isOpen, onClose, xpEarned = 50 }: ChallengeBonusModalProps) {
  useEffect(() => {
    if (isOpen) {
      confetti({
        particleCount: 150,
        spread: 80,
        origin: { y: 0.5 },
      });
    }
  }, [isOpen]);

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <motion.div
            className="w-full max-w-sm rounded-2xl bg-background border shadow-2xl p-8 text-center"
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: 'spring', stiffness: 300 }}
            >
              <Sparkles className="mx-auto h-16 w-16 text-amber-500" />
            </motion.div>

            <h2 className="mt-4 font-heading text-2xl font-bold">
              🎉 Daily Champion!
            </h2>

            <p className="mt-2 text-muted-foreground">
              You completed all 3 challenges!
            </p>

            <motion.div
              className="mt-4 rounded-xl bg-primary/10 p-4"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.4, type: 'spring' }}
            >
              <p className="text-sm text-muted-foreground">Bonus XP</p>
              <p className="font-heading text-3xl font-bold text-primary">
                +{xpEarned} XP
              </p>
            </motion.div>

            <Button onClick={onClose} size="lg" className="mt-6 w-full gap-2">
              Awesome! 🚀
            </Button>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

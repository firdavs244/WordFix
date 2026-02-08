import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, ArrowUp } from 'lucide-react';
import type { XPResult } from '@/types';

interface XPPopupProps {
  xpResult: XPResult | null;
  onDone?: () => void;
}

export function XPPopup({ xpResult, onDone }: XPPopupProps) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    if (xpResult && xpResult.xp_gained > 0) {
      setShow(true);
      const timer = setTimeout(() => {
        setShow(false);
        onDone?.();
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [xpResult, onDone]);

  return (
    <AnimatePresence>
      {show && xpResult && (
        <motion.div
          className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-white shadow-2xl shadow-primary/30"
          initial={{ opacity: 0, y: 40, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20, scale: 0.9 }}
          transition={{ type: 'spring', stiffness: 300, damping: 25 }}
        >
          <motion.div
            animate={{ rotate: [0, 15, -15, 0] }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <Zap className="h-5 w-5 fill-white" />
          </motion.div>
          <span className="font-heading text-lg font-bold">+{xpResult.xp_gained} XP</span>
          {xpResult.level_up && (
            <motion.div
              className="ml-1 flex items-center gap-1 rounded-lg bg-white/20 px-2 py-0.5"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.3, type: 'spring' }}
            >
              <ArrowUp className="h-4 w-4" />
              <span className="text-sm font-semibold">Level {xpResult.new_level}!</span>
            </motion.div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}

import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

interface ComboBreakEffectProps {
  onComplete: () => void;
}

export function ComboBreakEffect({ onComplete }: ComboBreakEffectProps) {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setShow(false);
      onComplete();
    }, 1200);
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <AnimatePresence>
      {show && (
        <>
          {/* Red flash overlay */}
          <motion.div
            className="pointer-events-none fixed inset-0 z-40 bg-red-500/10"
            initial={{ opacity: 1 }}
            animate={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          />

          {/* Combo Lost text */}
          <motion.div
            className="pointer-events-none fixed inset-0 z-50 flex items-start justify-center pt-32"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div
              className="rounded-xl bg-red-500/10 border border-red-500/30 px-6 py-3"
              animate={{
                x: [0, -8, 8, -6, 6, -3, 3, 0],
              }}
              transition={{ duration: 0.5 }}
            >
              <span className="font-heading text-lg font-bold text-red-500 dark:text-red-400">
                💔 Combo Lost!
              </span>
            </motion.div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

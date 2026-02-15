import { motion } from 'framer-motion';
import Logo from './Logo';

const dotVariants = {
  animate: (i: number) => ({
    y: [0, -8, 0],
    transition: { duration: 0.5, repeat: Infinity, repeatDelay: 0.6, delay: i * 0.15, ease: 'easeInOut' as const },
  }),
};

export default function LoadingScreen() {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background">
      <motion.div className="flex flex-col items-center gap-5" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <Logo size="lg" />
        <div className="flex gap-1.5">
          {[0, 1, 2].map((i) => (
            <motion.div key={i} custom={i} animate="animate" variants={dotVariants} className="h-2 w-2 rounded-full bg-primary" />
          ))}
        </div>
        <p className="text-sm text-muted-foreground">Loading...</p>
      </motion.div>
    </div>
  );
}

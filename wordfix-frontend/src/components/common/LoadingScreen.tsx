import { motion } from 'framer-motion';
import { Logo } from './Logo';

export function LoadingScreen() {
  return (
    <div className="flex h-screen w-screen items-center justify-center bg-background">
      <motion.div
        className="flex flex-col items-center gap-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Logo />
        <motion.div
          className="flex gap-1"
          initial="start"
          animate="end"
          variants={{
            start: { transition: { staggerChildren: 0.1 } },
            end: { transition: { staggerChildren: 0.1 } },
          }}
        >
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="h-2 w-2 rounded-full bg-primary"
              variants={{
                start: { y: 0, opacity: 0.4 },
                end: { y: -8, opacity: 1 },
              }}
              transition={{
                duration: 0.4,
                repeat: Infinity,
                repeatType: 'reverse',
                delay: i * 0.1,
              }}
            />
          ))}
        </motion.div>
        <p className="text-sm text-muted-foreground">Loading...</p>
      </motion.div>
    </div>
  );
}

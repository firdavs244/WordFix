import { motion } from 'framer-motion';

interface Props {
  progress: number;
}

export default function SessionProgressBar({ progress }: Props) {
  return (
    <div className="fixed left-0 top-14 z-20 h-1 w-full bg-muted">
      <motion.div
        className="h-full bg-gradient-to-r from-primary via-secondary to-primary"
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.4, ease: 'easeOut' }}
      />
    </div>
  );
}

import { motion } from 'framer-motion';

interface Props {
  onComplete?: () => void;
}

export default function ComboBreakEffect({ onComplete }: Props) {
  return (
    <motion.div
      className="pointer-events-none fixed inset-0 z-50 bg-destructive/10"
      initial={{ opacity: 0 }}
      animate={{ opacity: [0, 0.3, 0] }}
      transition={{ duration: 0.3 }}
      onAnimationComplete={onComplete}
    />
  );
}

import { motion } from 'framer-motion';

interface Props {
  value: number;
  color?: string;
  delay?: number;
}

export function LearningStyleBar({
  value,
  color = 'bg-primary',
  delay = 0,
}: Props) {
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
      <motion.div
        className={`h-full rounded-full ${color}`}
        initial={{ width: 0 }}
        animate={{ width: `${Math.min(value, 100)}%` }}
        transition={{ duration: 0.8, delay, ease: 'easeOut' }}
      />
    </div>
  );
}

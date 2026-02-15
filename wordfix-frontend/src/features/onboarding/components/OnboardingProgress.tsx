import { motion } from 'framer-motion';

interface Props {
  current: number;
  total: number;
}

export function OnboardingProgress({ current, total }: Props) {
  const pct = total > 0 ? (current / total) * 100 : 0;

  return (
    <div className="mb-8 w-full">
      <div className="h-1 overflow-hidden rounded-full bg-muted">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-primary to-secondary"
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        />
      </div>
      <p className="mt-2.5 text-center text-xs text-muted-foreground">
        Question <span className="font-semibold text-foreground">{current}</span> of {total}
      </p>
    </div>
  );
}

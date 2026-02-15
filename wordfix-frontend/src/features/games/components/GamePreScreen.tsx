import { motion } from 'framer-motion';
import { Play, Loader2, type LucideIcon } from 'lucide-react';
import { bounceIn } from '@/lib/motion';

interface Props {
  title: string;
  icon: LucideIcon;
  rules: string[];
  onStart: () => void;
  isLoading?: boolean;
}

export default function GamePreScreen({ title, icon: Icon, rules, onStart, isLoading }: Props) {
  return (
    <div className="mx-auto max-w-md py-12 text-center">
      <motion.div variants={bounceIn} initial="initial" animate="animate">
        <div className="mx-auto mb-6 flex h-[72px] w-[72px] animate-float items-center justify-center rounded-3xl bg-gradient-to-br from-primary to-primary/80 shadow-lg">
          <Icon className="h-9 w-9 text-white" />
        </div>
      </motion.div>

      <h2 className="font-heading text-2xl font-bold">{title}</h2>

      <div className="mt-6 space-y-3 text-left">
        {rules.map((rule, i) => (
          <div key={i} className="flex items-start gap-3">
            <span className="flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-bold text-primary">
              {i + 1}
            </span>
            <span className="text-sm text-muted-foreground">{rule}</span>
          </div>
        ))}
      </div>

      <motion.button
        type="button"
        onClick={onStart}
        disabled={isLoading}
        whileTap={{ scale: 0.98 }}
        whileHover={{ scale: 1.01 }}
        className="mt-8 flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/80 text-sm font-semibold text-white shadow-lg disabled:opacity-50"
      >
        {isLoading ? (
          <Loader2 className="h-5 w-5 animate-spin" />
        ) : (
          <>
            <Play className="h-5 w-5" /> Start Game
          </>
        )}
      </motion.button>
    </div>
  );
}

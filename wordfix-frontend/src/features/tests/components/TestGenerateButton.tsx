import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';

interface Props {
  onGenerate: () => void;
  isLoading: boolean;
  disabled?: boolean;
}

export default function TestGenerateButton({ onGenerate, isLoading, disabled }: Props) {
  return (
    <motion.button
      type="button"
      onClick={onGenerate}
      disabled={disabled || isLoading}
      whileTap={{ scale: 0.98 }}
      whileHover={{ scale: 1.01 }}
      className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary via-primary/95 to-secondary/80 text-sm font-semibold text-white shadow-lg shadow-primary/20 transition-shadow hover:shadow-xl hover:shadow-primary/30 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isLoading ? (
        <>
          <Loader2 className="h-[18px] w-[18px] animate-spin" />
          Generating with AI...
        </>
      ) : (
        <>
          <Sparkles className="h-[18px] w-[18px]" />
          Generate Test
        </>
      )}
    </motion.button>
  );
}

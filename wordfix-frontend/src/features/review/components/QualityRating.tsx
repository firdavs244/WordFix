import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import type { ReviewQuality } from '@/types';

interface QualityRatingProps {
  onRate: (quality: ReviewQuality) => void;
  disabled?: boolean;
}

const qualityOptions: { quality: ReviewQuality; label: string; description: string; color: string; emoji: string }[] = [
  { quality: 0, label: 'Again', description: 'No clue', color: 'bg-red-500 hover:bg-red-600', emoji: '😰' },
  { quality: 1, label: 'Hard', description: 'Wrong', color: 'bg-orange-500 hover:bg-orange-600', emoji: '😓' },
  { quality: 2, label: 'Difficult', description: 'Barely', color: 'bg-amber-500 hover:bg-amber-600', emoji: '🤔' },
  { quality: 3, label: 'Good', description: 'With effort', color: 'bg-yellow-500 hover:bg-yellow-600', emoji: '😊' },
  { quality: 4, label: 'Easy', description: 'Smooth', color: 'bg-emerald-500 hover:bg-emerald-600', emoji: '😄' },
  { quality: 5, label: 'Perfect', description: 'Instant', color: 'bg-green-500 hover:bg-green-600', emoji: '🤩' },
];

export function QualityRating({ onRate, disabled = false }: QualityRatingProps) {
  return (
    <div className="mx-auto w-full max-w-lg">
      <p className="mb-3 text-center text-sm font-medium text-muted-foreground">
        How well did you know this?
      </p>
      <div className="grid grid-cols-3 gap-2 sm:grid-cols-6">
        {qualityOptions.map((option, index) => (
          <motion.button
            key={option.quality}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            disabled={disabled}
            onClick={() => onRate(option.quality)}
            className={cn(
              'flex flex-col items-center gap-1 rounded-xl px-2 py-3 text-white transition-all',
              'shadow-md hover:shadow-lg active:scale-95',
              'disabled:opacity-50 disabled:cursor-not-allowed',
              option.color,
            )}
          >
            <span className="text-xl">{option.emoji}</span>
            <span className="text-xs font-semibold">{option.label}</span>
            <span className="hidden text-[10px] opacity-80 sm:block">
              {option.description}
            </span>
          </motion.button>
        ))}
      </div>
    </div>
  );
}

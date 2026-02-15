import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { cn } from '@/lib/utils';
import type { MistakePattern } from '@/types';

const TYPE_STYLES: Record<string, { label: string; className: string }> = {
  l1_interference: { label: 'Ona tili', className: 'bg-red-500/10 text-red-500 border-red-500/20' },
  morphological: { label: 'Shakl', className: 'bg-orange-500/10 text-orange-500 border-orange-500/20' },
  semantic: { label: "Ma'no", className: 'bg-yellow-500/10 text-yellow-600 border-yellow-500/20' },
  spelling: { label: 'Imlo', className: 'bg-blue-500/10 text-blue-500 border-blue-500/20' },
  phonological: { label: 'Talaffuz', className: 'bg-violet-500/10 text-violet-500 border-violet-500/20' },
};

export default function MistakePatternItem({ pattern }: { pattern: MistakePattern }) {
  const typeStyle = TYPE_STYLES[pattern.type] ?? TYPE_STYLES.spelling;

  return (
    <motion.div
      variants={staggerItem}
      className="flex items-center gap-3 rounded-xl p-3"
    >
      <span className={cn('shrink-0 rounded-full border px-2 py-0.5 text-[10px]', typeStyle.className)}>
        {typeStyle.label}
      </span>
      <p className="flex-1 text-sm line-clamp-1">{pattern.description}</p>
      <span className="shrink-0 text-xs font-medium text-muted-foreground">
        {pattern.occurrence_count} marta
      </span>
    </motion.div>
  );
}

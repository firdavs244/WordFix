import { motion } from 'framer-motion';
import type { BadgeCategory } from '@/types';

const CATEGORIES: { value: BadgeCategory | 'all'; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'words', label: 'Words' },
  { value: 'streak', label: 'Streak' },
  { value: 'review', label: 'Review' },
  { value: 'test', label: 'Tests' },
  { value: 'game', label: 'Games' },
  { value: 'mastery', label: 'Mastery' },
  { value: 'level', label: 'Level' },
];

interface BadgesCategoryFilterProps {
  activeCategory: string;
  onChange: (category: string) => void;
}

export default function BadgesCategoryFilter({ activeCategory, onChange }: BadgesCategoryFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {CATEGORIES.map((cat) => (
        <button
          key={cat.value}
          onClick={() => onChange(cat.value)}
          className="relative text-xs px-3.5 py-2 rounded-xl transition-all font-medium"
        >
          {activeCategory === cat.value && (
            <motion.div
              layoutId="badge-category-indicator"
              className="absolute inset-0 bg-primary rounded-xl shadow-sm"
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
            />
          )}
          <span
            className={`relative z-10 ${
              activeCategory === cat.value ? 'text-white font-semibold' : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {cat.label}
          </span>
        </button>
      ))}
    </div>
  );
}

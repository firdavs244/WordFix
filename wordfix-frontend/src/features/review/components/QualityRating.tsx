import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { fadeInUp } from '@/lib/motion';
import QualityButton from './QualityButton';
import type { ReviewQuality } from '@/types';

interface Props {
  onRate: (quality: ReviewQuality) => void;
}

const qualities = [
  { quality: 0 as ReviewQuality, emoji: '😫', label: 'Again', shortcut: '1' },
  { quality: 1 as ReviewQuality, emoji: '😰', label: 'Hard', shortcut: '2' },
  { quality: 2 as ReviewQuality, emoji: '😕', label: 'Difficult', shortcut: '3' },
  { quality: 3 as ReviewQuality, emoji: '🙂', label: 'Good', shortcut: '4' },
  { quality: 4 as ReviewQuality, emoji: '😄', label: 'Easy', shortcut: '5' },
  { quality: 5 as ReviewQuality, emoji: '🤩', label: 'Perfect', shortcut: '6' },
];

export default function QualityRating({ onRate }: Props) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const num = parseInt(e.key);
      if (num >= 1 && num <= 6) onRate((num - 1) as ReviewQuality);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onRate]);

  return (
    <motion.div variants={fadeInUp} initial="initial" animate="animate" className="mt-6 grid w-full grid-cols-3 gap-2 lg:grid-cols-6">
      {qualities.map((q) => (
        <QualityButton key={q.quality} {...q} onRate={onRate} />
      ))}
    </motion.div>
  );
}

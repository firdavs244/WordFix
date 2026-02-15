import { motion } from 'framer-motion';
import type { Word } from '@/types';
import FlashCardFront from './FlashCardFront';
import FlashCardBack from './FlashCardBack';

interface Props {
  word: Word;
  isFlipped: boolean;
  onFlip: () => void;
}

export default function FlashCard({ word, isFlipped, onFlip }: Props) {
  return (
    <div
      className="relative mx-auto aspect-[3/4] w-full max-h-[500px] cursor-pointer"
      onClick={onFlip}
      role="button"
      aria-label={isFlipped ? 'Flash card back' : 'Flash card front'}
    >
      <motion.div
        className="relative h-full w-full"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      >
        <FlashCardFront word={word} />
        <FlashCardBack word={word} />
      </motion.div>
    </div>
  );
}

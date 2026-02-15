import { motion } from 'framer-motion';
import { bounceIn } from '@/lib/motion';

interface Props {
  word: string;
}

export default function SpeedRoundWord({ word }: Props) {
  return (
    <motion.div variants={bounceIn} initial="initial" animate="animate" className="text-center">
      <p className="font-heading text-3xl font-bold lg:text-4xl">{word}</p>
      <p className="mt-1 text-sm text-muted-foreground">Choose the correct translation</p>
    </motion.div>
  );
}

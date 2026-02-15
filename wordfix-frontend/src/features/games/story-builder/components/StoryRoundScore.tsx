import { motion } from 'framer-motion';
import { Star } from 'lucide-react';
import { bounceIn } from '@/lib/motion';

interface Props {
  score: number;
  feedback: string;
}

export default function StoryRoundScore({ score, feedback }: Props) {
  return (
    <motion.div variants={bounceIn} initial="initial" animate="animate" className="mt-4 rounded-xl border border-accent/20 bg-accent/5 p-4 text-center">
      <div className="flex items-center justify-center gap-1.5">
        <Star className="h-5 w-5 text-accent" />
        <span className="font-heading text-xl font-bold text-accent">{score}/10</span>
      </div>
      <p className="mt-1 text-sm text-muted-foreground">{feedback}</p>
    </motion.div>
  );
}

import { motion } from 'framer-motion';
import { Bot } from 'lucide-react';
import { fadeIn } from '@/lib/motion';

export default function ChatTypingIndicator() {
  return (
    <motion.div variants={fadeIn} initial="initial" animate="animate" className="flex items-center gap-2.5 px-1">
      <div className="flex h-7 w-7 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-secondary/20">
        <Bot className="h-3.5 w-3.5 text-primary" />
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-bl-md border border-border/30 bg-card px-4 py-3">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1.5 w-1.5 animate-bounce rounded-full bg-muted-foreground/30"
            style={{ animationDelay: `${i * 0.15}s`, animationDuration: '0.6s' }}
          />
        ))}
      </div>
    </motion.div>
  );
}

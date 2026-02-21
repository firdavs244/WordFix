import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface ChatMessageBubbleProps {
  text: string;
  timestamp: string;
  side: 'left' | 'right';
}

export default function ChatMessageBubble({ text, timestamp, side }: ChatMessageBubbleProps) {
  const time = new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0, transition: { duration: 0.15 } }}
      className={cn(
        'max-w-[75%] px-4 py-2.5 text-sm leading-relaxed shadow-sm lg:max-w-[65%]',
        side === 'right'
          ? 'rounded-2xl rounded-br-md bg-primary text-white'
          : 'rounded-2xl rounded-bl-md border border-border/30 bg-card',
      )}
    >
      <p className="whitespace-pre-wrap">{text}</p>
      <p
        className={cn(
          'mt-1 text-[9px] text-right',
          side === 'right' ? 'text-white/50' : 'text-muted-foreground/40',
        )}
      >
        {time}
      </p>
    </motion.div>
  );
}

import { useState, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { SendHorizontal } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ChatInputAreaProps {
  onSend: (message: string) => void;
  disabled: boolean;
}

export default function ChatInputArea({ onSend, disabled }: ChatInputAreaProps) {
  const [text, setText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = useCallback(() => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
  }, [text, disabled, onSend]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    const el = e.target;
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
  };

  const hasText = text.trim().length > 0;

  return (
    <div className="border-t border-border/20 bg-background/80 px-4 py-3 backdrop-blur-xl">
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Type your message..."
          rows={1}
          className="max-h-[120px] min-h-[44px] flex-1 resize-none rounded-2xl border border-border/50 bg-card px-4 py-3 text-sm transition-all placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10 disabled:opacity-50"
        />
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={handleSend}
          disabled={!hasText || disabled}
          aria-label="Send message"
          className={cn(
            'flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition-all',
            hasText && !disabled
              ? 'bg-primary text-white shadow-sm hover:scale-105'
              : 'cursor-not-allowed bg-muted text-muted-foreground/30',
          )}
        >
          <SendHorizontal className="h-[18px] w-[18px]" />
        </motion.button>
      </div>
    </div>
  );
}

import { motion } from 'framer-motion';
import { MessageCircle, Loader2 } from 'lucide-react';

interface StartChatButtonProps {
  onClick: () => void;
  isLoading: boolean;
  disabled: boolean;
}

export default function StartChatButton({ onClick, isLoading, disabled }: StartChatButtonProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      disabled={disabled || isLoading}
      className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white shadow-lg shadow-primary/15 transition-all hover:shadow-xl hover:shadow-primary/25 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isLoading ? (
        <>
          <Loader2 className="h-[18px] w-[18px] animate-spin" />
          <span>Starting...</span>
        </>
      ) : (
        <>
          <MessageCircle className="h-[18px] w-[18px]" />
          <span>Start Conversation</span>
        </>
      )}
    </motion.button>
  );
}

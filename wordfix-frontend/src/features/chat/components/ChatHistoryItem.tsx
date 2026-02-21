import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MessageCircle } from 'lucide-react';
import { staggerItem } from '@/lib/motion';
import type { ChatSession } from '@/types';

interface ChatHistoryItemProps {
  session: ChatSession;
}

export default function ChatHistoryItem({ session }: ChatHistoryItemProps) {
  const navigate = useNavigate();

  return (
    <motion.div
      variants={staggerItem}
      onClick={() => navigate(`/chat/session/${session.id}`)}
      className="cursor-pointer rounded-xl border border-border/50 p-4 transition-all duration-200 hover:border-border hover:bg-muted/20 hover:shadow-card"
    >
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-primary/10">
          <MessageCircle className="h-[18px] w-[18px] text-primary" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate font-heading text-sm font-semibold">{session.topic || 'Free Conversation'}</p>
          <p className="mt-0.5 text-xs text-muted-foreground">
            {session.message_count} messages · {(session.words_practiced ?? []).length} words practiced
          </p>
        </div>
        <div className="shrink-0 text-right">
          {session.is_active ? (
            <span className="flex items-center gap-1 text-[10px] text-success">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              Active
            </span>
          ) : (
            <span className="text-[10px] text-muted-foreground/40">Ended</span>
          )}
          <p className="mt-1 text-[10px] text-muted-foreground/50">
            {new Date(session.started_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </motion.div>
  );
}

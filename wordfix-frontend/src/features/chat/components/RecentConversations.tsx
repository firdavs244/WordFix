import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { History, MessageCircle } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { EmptyState } from '@/components/shared';
import ConversationItem from './ConversationItem';
import type { ChatSession } from '@/types';

interface RecentConversationsProps {
  sessions: ChatSession[];
  isLoading: boolean;
}

export default function RecentConversations({ sessions, isLoading }: RecentConversationsProps) {
  if (isLoading) return null;

  return (
    <div>
      <div className="flex items-center gap-2">
        <History className="h-[18px] w-[18px] text-muted-foreground" />
        <h2 className="font-heading text-base font-semibold">Recent Conversations</h2>
      </div>

      {sessions.length === 0 ? (
        <EmptyState
          icon={MessageCircle}
          title="No conversations yet"
          description="Start a chat to practice your vocabulary"
        />
      ) : (
        <>
          <motion.div variants={staggerContainer} initial="initial" animate="animate" className="mt-4 space-y-2">
            {sessions.slice(0, 5).map((s) => (
              <ConversationItem key={s.id} conversation={s} />
            ))}
          </motion.div>
          <Link to="/chat/history" className="mt-3 inline-block text-xs text-primary hover:underline">
            View All History →
          </Link>
        </>
      )}
    </div>
  );
}

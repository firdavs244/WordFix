import { motion } from 'framer-motion';
import { MessageCircle } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { EmptyState } from '@/components/shared';
import ChatHistoryItem from './ChatHistoryItem';
import type { ChatSession } from '@/types';

interface ChatHistoryListProps {
  sessions: ChatSession[];
  isLoading: boolean;
}

export default function ChatHistoryList({ sessions, isLoading }: ChatHistoryListProps) {
  if (isLoading) return null;

  if (sessions.length === 0) {
    return (
      <EmptyState
        icon={MessageCircle}
        title="No chat sessions yet"
        description="Start a conversation to practice your vocabulary"
        action={{ label: 'Start Chat', href: '/chat' }}
      />
    );
  }

  return (
    <motion.div variants={staggerContainer} initial="initial" animate="animate" className="space-y-2">
      {sessions.map((s) => (
        <ChatHistoryItem key={s.id} session={s} />
      ))}
    </motion.div>
  );
}

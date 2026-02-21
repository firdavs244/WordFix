import { History } from 'lucide-react';
import { PageTransition, PageHeader } from '@/components/shared';
import ChatHistoryList from '../components/ChatHistoryList';
import { useChatHistory } from '../hooks/useChat';
import type { ChatSession } from '@/types';

export function ChatHistoryPage() {
  const { data, isLoading } = useChatHistory();
  const sessions: ChatSession[] = data?.data || [];

  return (
    <PageTransition>
      <PageHeader title="Chat History" icon={History} backLink="/chat" />
      <div className="mt-6">
        <ChatHistoryList sessions={sessions} isLoading={isLoading} />
      </div>
    </PageTransition>
  );
}

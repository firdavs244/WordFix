import { useNavigate } from 'react-router-dom';
import { MessageCircle } from 'lucide-react';
import { PageTransition, PageHeader } from '@/components/shared';
import ChatTopicSelector from '../components/ChatTopicSelector';
import RecentConversations from '../components/RecentConversations';
import { useStartChat, useChatHistory } from '../hooks/useChat';
import type { ChatSession } from '@/types';

export function ChatPage() {
  const navigate = useNavigate();
  const startChat = useStartChat();
  const { data: historyData, isLoading } = useChatHistory();
  const sessions: ChatSession[] = historyData?.data || [];

  const handleStart = async (topic: string) => {
    const result = await startChat.mutateAsync({ topic });
    navigate(`/chat/session/${result.data.session_id}`);
  };

  return (
    <PageTransition>
      <div className="space-y-8">
        <PageHeader title="AI Chat Practice" description="Practice vocabulary in real conversations with AI" icon={MessageCircle} />
        <ChatTopicSelector onStart={handleStart} isLoading={startChat.isPending} />
        <RecentConversations sessions={sessions} isLoading={isLoading} />
      </div>
    </PageTransition>
  );
}

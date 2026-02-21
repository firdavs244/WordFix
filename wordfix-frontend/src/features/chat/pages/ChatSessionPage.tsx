import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Loader2 } from 'lucide-react';
import ChatSessionHeader from '../components/ChatSessionHeader';
import ChatTargetWordsBar from '../components/ChatTargetWordsBar';
import ChatMessageArea from '../components/ChatMessageArea';
import ChatInputArea from '../components/ChatInputArea';
import { useChatSession, useEndChat } from '../hooks/useChat';
import { chatApi } from '../api/chatApi';
import type { ChatMessage } from '@/types';

export function ChatSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const { data: sessionData, isLoading } = useChatSession(sessionId || '');
  const endChat = useEndChat();

  const session = sessionData?.data?.session;
  const isEnded = !session?.is_active;

  useEffect(() => {
    if (sessionData?.data && !loaded) {
      setMessages(sessionData.data.messages || []);
      setLoaded(true);
    }
  }, [sessionData, loaded]);

  const usedWords = messages.flatMap((m) => m.words_used || []);

  const handleSend = async (text: string) => {
    if (!sessionId || isSending) return;
    setIsSending(true);
    const tempMsg: ChatMessage = { id: `t-${Date.now()}`, session_id: sessionId, role: 'user', content: text, corrections: [], words_used: [], order: messages.length, created_at: new Date().toISOString() };
    setMessages((p) => [...p, tempMsg]);
    try {
      const res = await chatApi.sendMessage(sessionId, { message: text });
      const d = res.data;
      const aiMsg: ChatMessage = { id: `a-${Date.now()}`, session_id: sessionId, role: 'assistant', content: d.ai_message, corrections: d.corrections || [], words_used: d.words_used || [], order: messages.length + 1, created_at: new Date().toISOString() };
      setMessages((p) => [...p.filter((m) => m.id !== tempMsg.id), { ...tempMsg, id: `u-${Date.now()}` }, aiMsg]);
    } catch { setMessages((p) => p.filter((m) => m.id !== tempMsg.id)); }
    finally { setIsSending(false); }
  };

  const handleEnd = async () => {
    if (!sessionId) return;
    await endChat.mutateAsync(sessionId);
    navigate('/chat');
  };

  if (isLoading) return <div className="flex h-full items-center justify-center"><Loader2 className="h-8 w-8 animate-spin text-primary" /></div>;

  return (
    <div className="flex min-h-screen flex-col bg-background">
      <ChatSessionHeader topic={session?.topic || 'Chat'} onEnd={handleEnd} isEnded={!!isEnded} />
      <ChatTargetWordsBar words={session?.target_words || []} usedWords={usedWords} />
      <ChatMessageArea messages={messages} isLoading={isSending} />
      <ChatInputArea onSend={handleSend} disabled={isSending || !!isEnded} />
    </div>
  );
}

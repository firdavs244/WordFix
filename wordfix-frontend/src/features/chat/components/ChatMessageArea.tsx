import { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatTypingIndicator from './ChatTypingIndicator';
import type { ChatMessage as MsgType } from '@/types';

interface ChatMessageAreaProps {
  messages: MsgType[];
  isLoading: boolean;
}

export default function ChatMessageArea({ messages, isLoading }: ChatMessageAreaProps) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 space-y-1 overflow-y-auto px-4 py-6 scrollbar-thin">
      {messages.length === 0 && !isLoading && (
        <p className="py-16 text-center text-sm text-muted-foreground/40">
          Send a message to start the conversation
        </p>
      )}
      {messages.map((msg, idx) => {
        const prev = messages[idx - 1];
        const showAvatar = msg.role === 'assistant' && (!prev || prev.role !== 'assistant');
        const isNewGroup = !prev || prev.role !== msg.role;
        return (
          <div key={msg.id} className={isNewGroup ? 'pt-3' : 'pt-0.5'}>
            <ChatMessage message={msg} showAvatar={showAvatar} />
          </div>
        );
      })}
      {isLoading && (
        <div className="pt-3">
          <ChatTypingIndicator />
        </div>
      )}
      <div ref={endRef} />
    </div>
  );
}

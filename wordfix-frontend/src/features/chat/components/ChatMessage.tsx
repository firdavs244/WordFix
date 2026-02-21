import { Bot } from 'lucide-react';
import ChatMessageBubble from './ChatMessageBubble';
import ChatCorrection from './ChatCorrection';
import type { ChatMessage as MsgType } from '@/types';

interface ChatMessageProps {
  message: MsgType;
  showAvatar?: boolean;
}

export default function ChatMessage({ message, showAvatar = true }: ChatMessageProps) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <ChatMessageBubble text={message.content} timestamp={message.created_at} side="right" />
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-end gap-2.5">
        {showAvatar ? (
          <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-secondary/20">
            <Bot className="h-3.5 w-3.5 text-primary" />
          </div>
        ) : (
          <div className="w-7" />
        )}
        <ChatMessageBubble text={message.content} timestamp={message.created_at} side="left" />
      </div>
      {message.corrections?.map((c, i) => (
        <ChatCorrection key={i} correction={c} />
      ))}
    </div>
  );
}

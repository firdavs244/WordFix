import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Bot, Square } from 'lucide-react';

interface ChatSessionHeaderProps {
  topic: string;
  onEnd: () => void;
  isEnded: boolean;
}

export default function ChatSessionHeader({ topic, onEnd, isEnded }: ChatSessionHeaderProps) {
  const navigate = useNavigate();

  return (
    <div className="sticky top-0 z-30 flex h-14 items-center justify-between border-b border-border/20 bg-background/80 px-4 backdrop-blur-xl lg:px-6">
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate('/chat')}
          className="flex h-9 w-9 items-center justify-center rounded-lg transition-colors hover:bg-muted"
        >
          <ArrowLeft className="h-[18px] w-[18px]" />
        </button>
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-primary to-secondary">
          <Bot className="h-4 w-4 text-white" />
        </div>
        <span className="max-w-[200px] truncate font-heading text-sm font-semibold">{topic}</span>
      </div>
      {!isEnded && (
        <button
          onClick={onEnd}
          className="flex h-8 items-center gap-1 rounded-lg px-3 text-xs font-medium text-destructive/70 transition-colors hover:bg-destructive/10 hover:text-destructive"
        >
          <Square className="h-3.5 w-3.5" />
          End Chat
        </button>
      )}
    </div>
  );
}

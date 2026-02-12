import { useState, useRef, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  Loader2,
  ArrowLeft,
  X,
  BookOpen,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Card } from '@/components/ui/card';
import { useChatSession, useEndChat } from '../hooks/useChat';
import { chatApi } from '../api/chatApi';
import type { ChatMessage, ChatCorrection } from '@/types';

export function ChatSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [targetWords, setTargetWords] = useState<string[]>([]);
  const [isSessionActive, setIsSessionActive] = useState(true);
  const [initialLoaded, setInitialLoaded] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { data: sessionData, isLoading } = useChatSession(sessionId || '');
  const endChat = useEndChat();

  // Load session data
  useEffect(() => {
    if (sessionData?.data && !initialLoaded) {
      setMessages(sessionData.data.messages || []);
      setTargetWords(sessionData.data.session.target_words || []);
      setIsSessionActive(sessionData.data.session.is_active);
      setInitialLoaded(true);
    }
  }, [sessionData, initialLoaded]);

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim() || !sessionId || isSending) return;

    const userMsg = message;
    setMessage('');
    setIsSending(true);

    // Optimistic: add user message
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      session_id: sessionId,
      role: 'user',
      content: userMsg,
      corrections: [],
      words_used: [],
      order: messages.length,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const result = await chatApi.sendMessage(sessionId, { message: userMsg });
      const data = result.data;
      // Keep user message (update id) and build AI message from response
      const aiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        session_id: sessionId,
        role: 'assistant',
        content: data.ai_message ?? '',
        corrections: data.corrections || [],
        words_used: data.words_used || [],
        order: messages.length + 1,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [
        ...prev.filter((m) => m.id !== tempUserMsg.id),
        { ...tempUserMsg, id: `user-${Date.now()}` },
        aiMsg,
      ]);
    } catch {
      // Remove temp message on error
      setMessages((prev) => prev.filter((m) => m.id !== tempUserMsg.id));
    } finally {
      setIsSending(false);
    }
  };

  const handleEndChat = async () => {
    if (!sessionId) return;
    await endChat.mutateAsync(sessionId);
    setIsSessionActive(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      {/* Chat Header */}
      <div className="flex items-center justify-between border-b p-4">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" onClick={() => navigate('/chat')}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h2 className="font-semibold text-foreground">
              {sessionData?.data?.session.topic || 'Free Conversation'}
            </h2>
            <p className="text-xs text-muted-foreground">
              {isSessionActive ? 'Active session' : 'Session ended'}
            </p>
          </div>
        </div>
        {isSessionActive && (
          <Button variant="outline" size="sm" onClick={handleEndChat} disabled={endChat.isPending}>
            <X className="mr-1 h-4 w-4" />
            End Chat
          </Button>
        )}
      </div>

      {/* Target Words Bar */}
      {targetWords.length > 0 && (
        <div className="flex items-center gap-2 border-b bg-muted/30 px-4 py-2">
          <BookOpen className="h-4 w-4 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Target words:</span>
          <div className="flex flex-wrap gap-1">
            {targetWords.map((w) => (
              <Badge key={w} variant="secondary" className="text-xs">
                {w}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="mx-auto max-w-3xl space-y-4">
          <AnimatePresence>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted text-foreground'
                  }`}
                >
                  <p className="whitespace-pre-wrap text-sm">{msg.content}</p>

                  {/* Corrections */}
                  {msg.corrections && msg.corrections.length > 0 && (
                    <div className="mt-2 space-y-1 border-t border-border/20 pt-2">
                      {msg.corrections.map((c: ChatCorrection, i: number) => (
                        <div key={i} className="flex items-start gap-1.5 text-xs">
                          <AlertCircle className="mt-0.5 h-3 w-3 shrink-0 text-yellow-500" />
                          <div>
                            <span className="line-through opacity-70">{c.original}</span>
                            {' → '}
                            <span className="font-medium">{c.corrected}</span>
                            {c.explanation && (
                              <span className="ml-1 opacity-70">({c.explanation})</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Words used */}
                  {msg.words_used && msg.words_used.length > 0 && (
                    <div className="mt-1 flex items-center gap-1">
                      <CheckCircle2 className="h-3 w-3 text-green-500" />
                      <span className="text-xs opacity-70">
                        Used: {msg.words_used.join(', ')}
                      </span>
                    </div>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {isSending && (
            <div className="flex justify-start">
              <div className="rounded-2xl bg-muted px-4 py-3">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Thinking...
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      {isSessionActive ? (
        <div className="border-t p-4">
          <div className="mx-auto flex max-w-3xl gap-2">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              disabled={isSending}
              className="flex-1"
            />
            <Button
              onClick={handleSend}
              disabled={!message.trim() || isSending}
              size="icon"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      ) : (
        <Card className="m-4 p-4 text-center text-sm text-muted-foreground">
          This session has ended. Start a new conversation from the Chat page.
        </Card>
      )}
    </div>
  );
}

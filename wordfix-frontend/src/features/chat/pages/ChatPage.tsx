import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MessageCircle, Plus, History, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useStartChat, useChatHistory } from '../hooks/useChat';
import type { ChatSession } from '@/types';

const TOPIC_SUGGESTIONS = [
  'Travel & Vacation',
  'Food & Cooking',
  'Technology & Science',
  'Movies & Entertainment',
  'Daily Life & Routines',
  'Work & Career',
];

export function ChatPage() {
  const navigate = useNavigate();
  const [topic, setTopic] = useState('');
  const startChat = useStartChat();
  const { data: historyData, isLoading: historyLoading } = useChatHistory();

  const handleStartChat = async (selectedTopic?: string) => {
    const result = await startChat.mutateAsync({
      topic: selectedTopic || topic || undefined,
    });
    navigate(`/chat/session/${result.data.session_id}`);
  };

  const recentSessions: ChatSession[] = historyData?.data || [];

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="font-heading text-3xl font-bold text-foreground">AI Chat</h1>
        <p className="mt-1 text-muted-foreground">
          Practice English conversation with an AI tutor using your vocabulary words
        </p>
      </motion.div>

      {/* Start new chat */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5 text-primary" />
              Start New Conversation
            </CardTitle>
            <CardDescription>
              Choose a topic or start a free conversation. The AI will naturally use words you&apos;re learning.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Topic chips */}
            <div className="flex flex-wrap gap-2">
              {TOPIC_SUGGESTIONS.map((t) => (
                <button
                  key={t}
                  onClick={() => setTopic(t)}
                  className={`rounded-full border px-3 py-1.5 text-sm transition-colors ${
                    topic === t
                      ? 'border-primary bg-primary/10 text-primary'
                      : 'border-border text-muted-foreground hover:border-primary/50'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>

            {/* Custom topic input */}
            <div className="flex gap-2">
              <Input
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Or type your own topic..."
                className="flex-1"
              />
              <Button
                onClick={() => handleStartChat()}
                disabled={startChat.isPending}
                size="lg"
              >
                {startChat.isPending ? (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                ) : (
                  <Sparkles className="mr-2 h-4 w-4" />
                )}
                Start Chat
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Recent sessions */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <History className="h-5 w-5 text-muted-foreground" />
                Recent Conversations
              </CardTitle>
              <Button variant="outline" size="sm" onClick={() => navigate('/chat/history')}>
                View All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {historyLoading ? (
              <div className="flex items-center justify-center py-8">
                <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
              </div>
            ) : recentSessions.length === 0 ? (
              <div className="py-8 text-center">
                <MessageCircle className="mx-auto h-10 w-10 text-muted-foreground/40" />
                <p className="mt-2 text-sm text-muted-foreground">No conversations yet. Start your first chat!</p>
              </div>
            ) : (
              <div className="space-y-2">
                {recentSessions.slice(0, 5).map((session) => (
                  <button
                    key={session.id}
                    onClick={() => navigate(`/chat/session/${session.id}`)}
                    className="flex w-full items-center justify-between rounded-lg border p-3 text-left transition-colors hover:bg-muted/50"
                  >
                    <div>
                      <p className="font-medium text-foreground">
                        {session.topic || 'Free Conversation'}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {session.message_count} messages • {new Date(session.started_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      {session.is_active && (
                        <span className="rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700 dark:bg-green-900/30 dark:text-green-400">
                          Active
                        </span>
                      )}
                      <span className="text-xs text-muted-foreground">
                        {(session.words_practiced ?? []).length} words practiced
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}

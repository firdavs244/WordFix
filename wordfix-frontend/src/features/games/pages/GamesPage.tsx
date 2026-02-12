import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Zap, Shuffle, BookOpen, History, TrendingUp, Headphones, PenTool } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { useGameHistory, useGameStats } from '../hooks/useGames';

const GAMES = [
  {
    key: 'speed_round',
    title: 'Speed Round',
    description: 'Answer as many questions as you can in 60 seconds!',
    icon: Zap,
    color: 'text-yellow-500',
    bg: 'bg-yellow-500/10',
    path: '/games/speed-round',
    bestLabel: (s: any) => s ? `Best: ${s.best_score}` : null,
  },
  {
    key: 'word_match',
    title: 'Word Match',
    description: 'Match words with their correct translations.',
    icon: Shuffle,
    color: 'text-blue-500',
    bg: 'bg-blue-500/10',
    path: '/games/word-match',
    bestLabel: (s: any) => s ? `Best: ${s.best_score}` : null,
  },
  {
    key: 'word_context',
    title: 'Word Context',
    description: 'Guess the word from a contextual paragraph.',
    icon: BookOpen,
    color: 'text-purple-500',
    bg: 'bg-purple-500/10',
    path: '/games/word-context',
    bestLabel: (s: any) => s ? `Best: ${s.best_score}` : null,
  },
  {
    key: 'story_builder',
    title: 'Story Builder',
    description: 'Write a story using your words.',
    icon: PenTool,
    color: 'text-violet-500',
    bg: 'bg-violet-500/10',
    path: '/games/story-builder',
    bestLabel: (s: any) => s ? `Best: ${s.best_score}/100` : null,
  },
  {
    key: 'listening_challenge',
    title: 'Listening Challenge',
    description: 'Listen and type the word you hear.',
    icon: Headphones,
    color: 'text-teal-500',
    bg: 'bg-teal-500/10',
    path: '/games/listening',
    bestLabel: (s: any) => s ? `Best: ${s.best_score}%` : null,
  },
] as const;

export function GamesPage() {
  const navigate = useNavigate();
  const { data: statsData } = useGameStats();
  const { data: historyData } = useGameHistory(1);

  const stats = statsData?.data;
  const recentGames = historyData?.data?.slice(0, 5) ?? [];

  return (
    <PageTransition>
      <div className="space-y-8">
        <div>
          <h1 className="text-2xl font-bold">Games</h1>
          <p className="text-muted-foreground">Learn vocabulary through fun games</p>
        </div>

        {/* Game Cards */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {GAMES.map((game, i) => {
            const gameStat = stats?.by_type?.[game.key];
            return (
              <motion.div
                key={game.key}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Card
                  className="cursor-pointer border-border/50 transition-all hover:shadow-md hover:-translate-y-1 hover:scale-[1.03]"
                  onClick={() => navigate(game.path)}
                >
                  <CardContent className="flex flex-col items-center gap-3 p-6 text-center">
                    <div className={`rounded-xl p-3 ${game.bg}`}>
                      <game.icon className={`h-8 w-8 ${game.color}`} />
                    </div>
                    <h3 className="font-semibold">{game.title}</h3>
                    <p className="text-sm text-muted-foreground">{game.description}</p>
                    {gameStat && gameStat.games_played > 0 && (
                      <p className="text-xs text-muted-foreground">
                        {game.bestLabel(gameStat)}
                      </p>
                    )}
                    <Button size="sm" className="mt-2 w-full">Play</Button>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>

        {/* Stats */}
        {stats && (
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <TrendingUp className="h-5 w-5" /> Your Stats
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-5">
                {GAMES.map((game) => {
                  const s = stats.by_type?.[game.key];
                  if (!s || s.games_played === 0) return (
                    <div key={game.key} className="rounded-lg border p-4 text-center">
                      <p className="text-sm font-medium">{game.title}</p>
                      <p className="mt-1 text-xs text-muted-foreground">No games yet</p>
                    </div>
                  );
                  return (
                    <div key={game.key} className="rounded-lg border p-4 text-center">
                      <p className="text-sm font-medium">{game.title}</p>
                      <p className="mt-1 text-2xl font-bold">{s.games_played}</p>
                      <p className="text-xs text-muted-foreground">games played</p>
                      <div className="mt-2 flex justify-center gap-3 text-xs text-muted-foreground">
                        <span>Best: {s.best_score}</span>
                        <span>XP: {s.total_xp}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Recent Games */}
        {recentGames.length > 0 && (
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <History className="h-5 w-5" /> Recent Games
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {recentGames.map((g: any) => (
                <div key={g.id} className="flex items-center justify-between rounded-lg border p-3">
                  <div>
                    <p className="text-sm font-medium capitalize">{g.game_type.replace('_', ' ')}</p>
                    <p className="text-xs text-muted-foreground">
                      {new Date(g.created_at).toLocaleDateString()} · Level {g.level}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-semibold">{g.score}/{g.max_score}</p>
                    <p className="text-xs text-muted-foreground">+{g.xp_earned} XP</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </div>
    </PageTransition>
  );
}

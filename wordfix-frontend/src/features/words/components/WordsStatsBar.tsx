import { BookOpen, CheckCircle2, Clock, Sparkles } from 'lucide-react';
import WordsStatPill from './WordsStatPill';
import { useWordStats } from '../hooks/useWords';

export default function WordsStatsBar() {
  const { data, isLoading } = useWordStats();
  const stats = data?.data;

  if (isLoading) {
    return (
      <div className="flex gap-3 overflow-x-auto pb-1 scrollbar-none" data-testid="stats-loading">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-14 w-36 shrink-0 animate-pulse rounded-xl bg-muted" />
        ))}
      </div>
    );
  }

  return (
    <div className="flex gap-3 overflow-x-auto pb-1 scrollbar-none">
      <WordsStatPill label="Total" value={stats?.total ?? 0} color="primary" icon={BookOpen} />
      <WordsStatPill label="Mastered" value={stats?.mastered ?? 0} color="success" icon={CheckCircle2} />
      <WordsStatPill label="Learning" value={stats?.learning ?? 0} color="warning" icon={Clock} />
      <WordsStatPill label="New" value={stats?.new ?? 0} color="secondary" icon={Sparkles} />
    </div>
  );
}

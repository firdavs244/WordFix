import { motion } from 'framer-motion';
import {
  BookOpen,
  Flame,
  Trophy,
  Loader2,
  Zap,
  Star,
  Target,
  Clock,
  Gamepad2,
  ClipboardCheck,
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  useAnalyticsOverview,
  useWeeklyStats,
  useDifficultWords,
  useWordProgress,
  useStudyCalendar,
} from '../hooks/useAnalytics';
import { StatCard } from '../components/StatCard';
import { WeeklyChart } from '../components/WeeklyChart';
import { StudyCalendar } from '../components/StudyCalendar';
import { DifficultWordsList } from '../components/DifficultWordsList';
import { WordDistribution } from '../components/WordDistribution';

// ─── Main Analytics Page ───────────────────────────────────────────────────────

export function AnalyticsPage() {
  const { data: overview, isLoading: overviewLoading } = useAnalyticsOverview();
  const { data: weekly } = useWeeklyStats();
  const { data: difficult } = useDifficultWords();
  const { data: progress } = useWordProgress();
  const { data: calendar } = useStudyCalendar();

  if (overviewLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const stats = overview?.data;
  const weeklyData = weekly?.data || [];
  const difficultWords = difficult?.data || [];
  const progressData = progress?.data;
  const calendarData = calendar?.data || [];

  return (
    <div className="mx-auto max-w-6xl space-y-6 p-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="font-heading text-3xl font-bold text-foreground">Analytics</h1>
        <p className="mt-1 text-muted-foreground">
          Track your learning progress and identify areas for improvement
        </p>
      </motion.div>

      {/* Overview Stats Grid */}
      {stats && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-2 gap-4 md:grid-cols-4"
        >
          <StatCard
            icon={<BookOpen className="h-5 w-5" />}
            label="Total Words"
            value={stats.total_words}
            subtitle={`${stats.mastered_words} mastered (${stats.mastered_percentage}%)`}
          />
          <StatCard
            icon={<Flame className="h-5 w-5" />}
            label="Current Streak"
            value={`${stats.current_streak} days`}
            subtitle={`Best: ${stats.longest_streak} days`}
            color="text-orange-500"
          />
          <StatCard
            icon={<Target className="h-5 w-5" />}
            label="Accuracy"
            value={`${stats.overall_accuracy}%`}
            subtitle={`${stats.total_reviews} total reviews`}
            color="text-green-500"
          />
          <StatCard
            icon={<Zap className="h-5 w-5" />}
            label="Total XP"
            value={stats.total_xp.toLocaleString()}
            subtitle={`Level ${stats.current_level}`}
            color="text-yellow-500"
          />
        </motion.div>
      )}

      {/* Second row stats */}
      {stats && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="grid grid-cols-2 gap-4 md:grid-cols-4"
        >
          <StatCard
            icon={<Clock className="h-5 w-5" />}
            label="Study Time"
            value={stats.total_study_time_formatted}
            color="text-blue-500"
          />
          <StatCard
            icon={<ClipboardCheck className="h-5 w-5" />}
            label="Tests Completed"
            value={stats.tests_completed}
            color="text-purple-500"
          />
          <StatCard
            icon={<Gamepad2 className="h-5 w-5" />}
            label="Games Played"
            value={stats.games_played}
            color="text-pink-500"
          />
          <StatCard
            icon={<Star className="h-5 w-5" />}
            label="Daily Average"
            value={`${stats.avg_daily_words} words`}
            subtitle={`Member for ${stats.member_since_days} days`}
            color="text-cyan-500"
          />
        </motion.div>
      )}

      {/* Charts Row */}
      <div className="grid gap-6 md:grid-cols-2">
        {weeklyData.length > 0 && <WeeklyChart data={weeklyData} />}
        {calendarData.length > 0 && <StudyCalendar data={calendarData} />}
      </div>

      {/* Progress and Difficult Words */}
      <div className="grid gap-6 md:grid-cols-2">
        {progressData && (
          <WordDistribution
            byConfidence={progressData.by_confidence}
            byDifficulty={progressData.by_difficulty}
          />
        )}
        <DifficultWordsList words={difficultWords} />
      </div>

      {/* Needs Attention */}
      {progressData && progressData.needs_attention.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <Trophy className="h-4 w-4 text-primary" />
              Needs Attention
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {progressData.needs_attention.map((item) => (
                <div
                  key={item.word}
                  className="rounded-full border border-yellow-200 bg-yellow-50 px-3 py-1 text-sm dark:border-yellow-900 dark:bg-yellow-900/20"
                >
                  <span className="font-medium text-foreground">{item.word}</span>
                  <span className="ml-1 text-muted-foreground">({item.accuracy}%)</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

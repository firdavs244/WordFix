import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  BookOpen,
  Target,
  ArrowRight,
  Zap,
  TrendingUp,
  CheckCircle2,
  Brain,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { PageTransition } from '@/components/animations/PageTransition';
import {
  cardHoverVariants,
  listContainerVariants,
  listItemVariants,
} from '@/components/animations/PageTransition';
import { useAuthStore } from '@/stores/useAuthStore';
import { useWordStats, useWords } from '@/features/words/hooks/useWords';
import { StreakWidget, DailyProgressWidget } from '@/features/review/components';
import { useReviewSummary } from '@/features/review/hooks/useReview';
import { LevelProgress } from '@/features/progress/components/LevelProgress';
import { XPChart } from '@/features/progress/components/XPChart';
import { DailyChallengesWidget } from '@/features/challenges/components/DailyChallengesWidget';
import { DomainCoverageWidget } from '@/features/learning/components/DomainCoverageWidget';
import { RecommendationsWidget } from '@/features/learning/components/RecommendationsWidget';
import { MistakePatternsWidget } from '@/features/learning/components/MistakePatternsWidget';
import { DashboardQuickActions } from '../components/DashboardQuickActions';
import { DashboardRecentWords } from '../components/DashboardRecentWords';

export function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const { data: statsData, isLoading: statsLoading } = useWordStats();
  const { data: recentData, isLoading: recentLoading } = useWords({
    page: 1,
    page_size: 5,
    ordering: '-created_at',
  });

  const stats = statsData?.data;
  const recentWords = recentData?.data ?? [];
  const { data: summaryData } = useReviewSummary();
  const summary = summaryData?.data;

  const statsCards = [
    {
      label: 'Total Words',
      value: stats?.total ?? 0,
      icon: BookOpen,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      sub: `${stats?.mastered ?? 0} mastered`,
    },
    {
      label: 'Learning',
      value: stats?.learning ?? 0,
      icon: TrendingUp,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
      sub: 'In progress',
    },
    {
      label: 'Daily Goal',
      value: `${user?.daily_goal ?? 10}`,
      icon: Target,
      color: 'text-success',
      bgColor: 'bg-success/10',
      sub: 'words / day',
    },
  ];

  return (
    <PageTransition>
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Welcome */}
        <motion.div
          className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div>
            <h1 className="font-heading text-3xl font-bold">
              Welcome back, {user?.full_name || user?.username || 'Learner'}! 👋
            </h1>
            <p className="mt-1 text-muted-foreground">Ready to learn some new words today?</p>
          </div>
          <Link to="/words">
            <Button size="lg" className="gap-2 shadow-lg shadow-primary/25">
              <Zap className="h-5 w-5" />
              Start Learning
              <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
        </motion.div>

        {/* Streak & Progress */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <LevelProgress />
          <StreakWidget />
          <DailyProgressWidget />
        </div>

        <DailyChallengesWidget />
        <XPChart />

        {/* Review CTA */}
        {summary && summary.words_due > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
          >
            <Card className="border-primary/30 bg-primary/5">
              <CardContent className="flex items-center gap-4 p-5">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                  <Brain className="h-6 w-6 text-primary" />
                </div>
                <div className="flex-1">
                  <p className="font-heading text-lg font-semibold">
                    {summary.words_due} words due for review
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Keep your streak going — review now!
                  </p>
                </div>
                <Link to="/review">
                  <Button className="gap-2 shadow-lg shadow-primary/25">
                    <Brain className="h-4 w-4" />
                    Review Now
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          </motion.div>
        )}

        <DashboardQuickActions />

        {/* Stats Cards */}
        {statsLoading ? (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <Card key={i} className="border-border/50">
                <CardContent className="p-6">
                  <Skeleton className="h-12 w-12 rounded-xl" />
                  <Skeleton className="mt-3 h-6 w-20" />
                  <Skeleton className="mt-1 h-4 w-32" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <motion.div
            className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {statsCards.map((stat) => (
              <motion.div key={stat.label} variants={listItemVariants}>
                <motion.div
                  variants={cardHoverVariants}
                  initial="rest"
                  whileHover="hover"
                  whileTap="tap"
                >
                  <Card className="cursor-pointer border-border/50">
                    <CardContent className="flex items-center gap-4 p-6">
                      <div
                        className={`flex h-12 w-12 items-center justify-center rounded-xl ${stat.bgColor}`}
                      >
                        <stat.icon className={`h-6 w-6 ${stat.color}`} />
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-muted-foreground">{stat.label}</p>
                        <p className="font-heading text-2xl font-bold">{stat.value}</p>
                        <p className="text-xs text-muted-foreground">{stat.sub}</p>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Confidence Score */}
        {stats && stats.total > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.2 }}
          >
            <Card className="border-border/50">
              <CardContent className="flex items-center gap-6 p-6">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
                  <CheckCircle2 className="h-7 w-7 text-primary" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground">Average Confidence</p>
                  <div className="mt-1 flex items-center gap-3">
                    <div className="h-3 flex-1 overflow-hidden rounded-full bg-muted">
                      <motion.div
                        className="h-full rounded-full bg-primary"
                        initial={{ width: 0 }}
                        animate={{ width: `${stats.average_confidence}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut' }}
                      />
                    </div>
                    <span className="font-heading text-lg font-bold">
                      {stats.average_confidence}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Domain Coverage */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.22 }}
        >
          <DomainCoverageWidget />
        </motion.div>

        {/* Recommendations & Mistakes */}
        <motion.div
          className="grid gap-4 md:grid-cols-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.25 }}
        >
          <RecommendationsWidget />
          <MistakePatternsWidget />
        </motion.div>

        <DashboardRecentWords words={recentWords} isLoading={recentLoading} />
      </div>
    </PageTransition>
  );
}

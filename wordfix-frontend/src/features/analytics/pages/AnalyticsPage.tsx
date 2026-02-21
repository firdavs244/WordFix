import { BarChart3 } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import { PageTransition, PageHeader } from '@/components/shared';
import AnalyticsOverview from '../components/AnalyticsOverview';
import WeeklyChart from '../components/WeeklyChart';
import StudyCalendar from '../components/StudyCalendar';
import WordDistribution from '../components/WordDistribution';
import DifficultWordsList from '../components/DifficultWordsList';
import {
  useAnalyticsOverview,
  useWeeklyStats,
  useStudyCalendar,
  useWordProgress,
  useDifficultWords,
} from '../hooks/useAnalytics';

function LoadingSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <Skeleton key={i} className="h-24 rounded-xl" />
        ))}
      </div>
      <Skeleton className="h-48 rounded-2xl" />
      <Skeleton className="h-32 rounded-2xl" />
    </div>
  );
}

export default function AnalyticsPage() {
  const overview = useAnalyticsOverview();
  const weekly = useWeeklyStats();
  const calendar = useStudyCalendar();
  const wordProgress = useWordProgress();
  const difficult = useDifficultWords();

  const isLoading =
    overview.isLoading || weekly.isLoading || calendar.isLoading || wordProgress.isLoading || difficult.isLoading;

  return (
    <PageTransition>
      <div className="mx-auto max-w-4xl space-y-6">
        <PageHeader title="Analytics" description="Track your learning progress" icon={BarChart3} />

        {isLoading ? (
          <LoadingSkeleton />
        ) : (
          <div className="space-y-6">
            {overview.data?.data && <AnalyticsOverview data={overview.data.data} />}

            {weekly.data?.data && <WeeklyChart data={weekly.data.data} />}

            {calendar.data?.data && <StudyCalendar data={calendar.data.data} />}

            {wordProgress.data?.data && <WordDistribution data={wordProgress.data.data} />}

            {difficult.data?.data && (
              <DifficultWordsList words={difficult.data.data} />
            )}
          </div>
        )}
      </div>
    </PageTransition>
  );
}

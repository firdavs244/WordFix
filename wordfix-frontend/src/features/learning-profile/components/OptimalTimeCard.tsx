import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Clock } from 'lucide-react';
import { OptimalDayIndicator } from './OptimalDayIndicator';
import { dayLabels } from './learningProfileHelpers';
import type { LearningProfile } from '@/types/learning';

interface Props {
  profile: LearningProfile | null;
  isLoading: boolean;
  hasAnalyzed: boolean;
}

export function OptimalTimeCard({ profile, isLoading, hasAnalyzed }: Props) {
  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Clock className="h-5 w-5 text-muted-foreground" />
          Optimal Time
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-8 w-full" />
          </div>
        ) : !hasAnalyzed ? (
          <p className="text-sm text-muted-foreground">
            Run an analysis to find your optimal study time
          </p>
        ) : profile?.best_time ? (
          <div className="space-y-4">
            <p className="text-lg font-semibold">
              Best hours:{' '}
              <span className="text-primary">
                {String(profile.best_time.start_hour).padStart(2, '0')}:00 –{' '}
                {String(profile.best_time.end_hour).padStart(2, '0')}:00
              </span>
            </p>

            <div className="flex gap-2">
              {dayLabels.map((day, i) => (
                <OptimalDayIndicator
                  key={day}
                  label={day}
                  isActive={profile.best_time.best_days.includes(i)}
                />
              ))}
            </div>

            {profile.session_stats && (
              <p className="text-xs text-muted-foreground">
                Avg session: {profile.session_stats.avg_duration} min ·
                Retention: {Math.round(profile.session_stats.retention_rate * 100)}%
              </p>
            )}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}

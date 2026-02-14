import { motion } from 'framer-motion';
import { Clock, Zap, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { PageTransition } from '@/components/animations/PageTransition';
import {
  useLearningProfile,
  useAnalyzeProfile,
  useMistakePatterns,
  useWordRecommendations,
  useDomainCoverage,
  useAcceptRecommendation,
} from '../hooks/useLearning';
import {
  containerVariants,
  sectionVariants,
  dayLabels,
  skillLabels,
  formatTimeAgo,
} from '../components/learningProfileHelpers';
import { LearningStyleCard, AnimatedBar } from '../components/LearningStyleCard';
import { LearningRecommendations } from '../components/LearningRecommendations';
import { LearningMistakes } from '../components/LearningMistakes';

// ─── Page Component ────────────────────────────────────────────────────────────

export function LearningProfilePage() {
  const { data: profileData, isLoading: profileLoading } = useLearningProfile();
  const analyze = useAnalyzeProfile();
  const { data: mistakesData, isLoading: mistakesLoading } = useMistakePatterns();
  const { data: recsData, isLoading: recsLoading } = useWordRecommendations();
  const { data: coverageData } = useDomainCoverage();
  const acceptRec = useAcceptRecommendation();

  const profile = profileData?.data;
  const mistakes = mistakesData?.data ?? [];
  const recommendations = recsData?.data ?? [];
  void coverageData;

  const hasAnalyzed = !!profile?.last_analyzed;

  return (
    <PageTransition>
      <motion.div
        className="mx-auto max-w-5xl space-y-8"
        variants={containerVariants}
        initial="hidden"
        animate="show"
      >
        {/* ── Header + Analyze Button ─────────────────────────────────────── */}
        <motion.div
          variants={sectionVariants}
          className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
        >
          <div>
            <h1 className="font-heading text-3xl font-bold">🧠 Learning Profile</h1>
            <p className="mt-1 text-muted-foreground">
              AI sizning o&apos;rganish uslubingizni tahlil qiladi
            </p>
          </div>
          <div className="flex flex-col items-start gap-1 sm:items-end">
            <Button
              onClick={() => analyze.mutate()}
              disabled={analyze.isPending}
              size="lg"
              className="gap-2 shadow-lg shadow-primary/25"
            >
              {analyze.isPending ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Tahlil qilinmoqda...
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5" />
                  Profilni tahlil qilish
                </>
              )}
            </Button>
            {hasAnalyzed && (
              <span className="text-xs text-muted-foreground">
                Oxirgi tahlil: {formatTimeAgo(profile.last_analyzed)}
              </span>
            )}
          </div>
        </motion.div>

        {/* ── Learning Style ──────────────────────────────────────────────── */}
        <LearningStyleCard
          profile={profile}
          profileLoading={profileLoading}
          hasAnalyzed={hasAnalyzed}
          onAnalyze={() => analyze.mutate()}
          analyzeIsPending={analyze.isPending}
        />

        {/* ── Optimal Time + Skills ───────────────────────────────────────── */}
        <motion.div variants={sectionVariants} className="grid gap-6 md:grid-cols-2">
          {/* Optimal Time */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Clock className="h-5 w-5 text-muted-foreground" />
                Optimal vaqt
              </CardTitle>
            </CardHeader>
            <CardContent>
              {profileLoading ? (
                <div className="space-y-3">
                  <Skeleton className="h-6 w-48" />
                  <Skeleton className="h-8 w-full" />
                </div>
              ) : !hasAnalyzed ? (
                <p className="text-sm text-muted-foreground">Tahlildan keyin aniqlanadi</p>
              ) : profile?.best_time ? (
                <div className="space-y-4">
                  <p className="text-lg font-semibold">
                    Eng samarali vaqtingiz:{' '}
                    <span className="text-primary">
                      {String(profile.best_time.start_hour).padStart(2, '0')}:00 -{' '}
                      {String(profile.best_time.end_hour).padStart(2, '0')}:00
                    </span>
                  </p>
                  <div className="flex gap-2">
                    {dayLabels.map((day, i) => {
                      const isActive = profile.best_time.best_days.includes(i);
                      return (
                        <div
                          key={day}
                          className={`flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition-colors ${
                            isActive
                              ? 'bg-primary text-primary-foreground'
                              : 'bg-muted text-muted-foreground'
                          }`}
                        >
                          {day}
                        </div>
                      );
                    })}
                  </div>
                  {profile.session_stats && (
                    <p className="text-xs text-muted-foreground">
                      O&apos;rtacha sessiya: {profile.session_stats.avg_duration} daqiqa · Saqlash:{' '}
                      {Math.round(profile.session_stats.retention_rate * 100)}%
                    </p>
                  )}
                </div>
              ) : null}
            </CardContent>
          </Card>

          {/* Skills */}
          <Card className="border-border/50">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Zap className="h-5 w-5 text-muted-foreground" />
                Ko&apos;nikmalar
              </CardTitle>
            </CardHeader>
            <CardContent>
              {profileLoading ? (
                <div className="space-y-3">
                  {[1, 2, 3, 4, 5].map((i) => (
                    <Skeleton key={i} className="h-6 w-full" />
                  ))}
                </div>
              ) : !hasAnalyzed ? (
                <p className="text-sm text-muted-foreground">Tahlildan keyin aniqlanadi</p>
              ) : profile?.skills ? (
                <div className="space-y-4">
                  {Object.entries(skillLabels).map(([key, label], i) => {
                    const score = profile.skills.scores?.[key] ?? 0;
                    const isStrong = profile.skills.strongest.includes(key);
                    const isWeak = profile.skills.weakest.includes(key);
                    return (
                      <div key={key} className="space-y-1.5">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium">{label}</span>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-muted-foreground">
                              {Math.round(score)}%
                            </span>
                            {isStrong && (
                              <Badge
                                variant="outline"
                                className="border-green-300 bg-green-50 text-green-700 dark:border-green-800 dark:bg-green-950 dark:text-green-300"
                              >
                                💪 Kuchli
                              </Badge>
                            )}
                            {isWeak && (
                              <Badge
                                variant="outline"
                                className="border-red-300 bg-red-50 text-red-700 dark:border-red-800 dark:bg-red-950 dark:text-red-300"
                              >
                                📚 Mashq kerak
                              </Badge>
                            )}
                          </div>
                        </div>
                        <AnimatedBar
                          value={score}
                          color={isStrong ? 'bg-green-500' : isWeak ? 'bg-red-400' : 'bg-primary'}
                          delay={i * 0.05}
                        />
                      </div>
                    );
                  })}
                </div>
              ) : null}
            </CardContent>
          </Card>
        </motion.div>

        {/* ── Word Recommendations ────────────────────────────────────────── */}
        <LearningRecommendations
          recommendations={recommendations}
          isLoading={recsLoading}
          onAccept={(id: string) => acceptRec.mutate(id)}
          acceptIsPending={acceptRec.isPending}
        />

        {/* ── Mistake Patterns ────────────────────────────────────────────── */}
        <LearningMistakes mistakes={mistakes} isLoading={mistakesLoading} />
      </motion.div>
    </PageTransition>
  );
}

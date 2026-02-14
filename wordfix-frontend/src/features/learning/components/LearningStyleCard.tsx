import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import {
  styleConfig,
  styleBarColors,
  sectionVariants,
} from './learningProfileHelpers';

// ─── Animated Bar ──────────────────────────────────────────────────────────────

function AnimatedBar({
  value,
  color,
  delay = 0,
}: {
  value: number;
  color: string;
  delay?: number;
}) {
  return (
    <div className="h-3 flex-1 overflow-hidden rounded-full bg-muted">
      <motion.div
        className={`h-full rounded-full ${color}`}
        initial={{ width: 0 }}
        animate={{ width: `${Math.min(value, 100)}%` }}
        transition={{ duration: 1, ease: 'easeOut', delay }}
      />
    </div>
  );
}

export { AnimatedBar };

// ─── Props ─────────────────────────────────────────────────────────────────────

interface LearningStyleCardProps {
  profile: {
    preferred_style: string;
    style_confidence: number;
    skills?: { scores?: Record<string, number> };
    last_analyzed: string | null;
  } | undefined;
  profileLoading: boolean;
  hasAnalyzed: boolean;
  onAnalyze: () => void;
  analyzeIsPending: boolean;
}

// ─── Component ─────────────────────────────────────────────────────────────────

export function LearningStyleCard({
  profile,
  profileLoading,
  hasAnalyzed,
  onAnalyze,
  analyzeIsPending,
}: LearningStyleCardProps) {
  return (
    <motion.div variants={sectionVariants}>
      <Card className="border-border/50">
        <CardHeader>
          <CardTitle className="text-xl">📖 O&apos;rganish uslubi</CardTitle>
        </CardHeader>
        <CardContent>
          {profileLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-12 w-48" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          ) : !hasAnalyzed ? (
            <div className="flex flex-col items-center gap-4 py-8 text-center">
              <p className="text-muted-foreground">
                Profilni tahlil qiling — AI sizning uslubingizni aniqlaydi
              </p>
              <Button
                onClick={onAnalyze}
                disabled={analyzeIsPending}
                className="gap-2"
              >
                <Sparkles className="h-4 w-4" />
                Tahlil qilish
              </Button>
            </div>
          ) : profile ? (
            <div className="space-y-6">
              {/* Main style */}
              <div className="flex items-center gap-4">
                {(() => {
                  const cfg = styleConfig[profile.preferred_style] ?? styleConfig.visual;
                  const Icon = cfg.icon;
                  return (
                    <>
                      <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
                        <Icon className={`h-7 w-7 ${cfg.color}`} />
                      </div>
                      <div>
                        <p className="font-heading text-xl font-bold">{cfg.label}</p>
                        <p className="text-sm text-muted-foreground">
                          Ishonchlilik: {Math.round(profile.style_confidence * 100)}%
                        </p>
                      </div>
                    </>
                  );
                })()}
              </div>

              {/* Confidence bar */}
              <div>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Ishonchlilik darajasi</span>
                  <span className="font-medium">{Math.round(profile.style_confidence * 100)}%</span>
                </div>
                <AnimatedBar value={profile.style_confidence * 100} color="bg-primary" />
              </div>

              {/* Breakdown */}
              {profile.skills?.scores && (
                <div className="space-y-3">
                  <p className="text-sm font-medium text-muted-foreground">Uslub taqsimoti</p>
                  {Object.entries(styleConfig).map(([key, cfg], i) => {
                    const value = profile.skills?.scores?.[key] ?? 0;
                    return (
                      <div key={key} className="flex items-center gap-3">
                        <span className="w-24 text-sm">{cfg.label.split(' ')[0]}</span>
                        <AnimatedBar value={value} color={styleBarColors[key]} delay={i * 0.05} />
                        <span className="w-10 text-right text-sm font-medium">{Math.round(value)}%</span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          ) : null}
        </CardContent>
      </Card>
    </motion.div>
  );
}

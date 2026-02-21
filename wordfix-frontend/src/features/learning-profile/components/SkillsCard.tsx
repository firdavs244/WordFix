import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Zap } from 'lucide-react';
import { SkillBar } from './SkillBar';
import { skillLabels } from './learningProfileHelpers';
import type { LearningProfile } from '@/types/learning';

interface Props {
  profile: LearningProfile | null;
  isLoading: boolean;
  hasAnalyzed: boolean;
}

export function SkillsCard({ profile, isLoading, hasAnalyzed }: Props) {
  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Zap className="h-5 w-5 text-muted-foreground" />
          Skills
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <Skeleton key={i} className="h-6 w-full" />
            ))}
          </div>
        ) : !hasAnalyzed ? (
          <p className="text-sm text-muted-foreground">
            Run an analysis to see your skill breakdown
          </p>
        ) : profile?.skills ? (
          <div className="space-y-4">
            {Object.entries(skillLabels).map(([key, label], i) => (
              <SkillBar
                key={key}
                name={key}
                label={label}
                score={profile.skills.scores?.[key] ?? 0}
                isStrong={profile.skills.strongest.includes(key)}
                isWeak={profile.skills.weakest.includes(key)}
                delay={i * 0.05}
              />
            ))}
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}

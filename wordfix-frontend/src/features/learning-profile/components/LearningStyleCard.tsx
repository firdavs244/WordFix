import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Palette } from 'lucide-react';
import { LearningStyleBar } from './LearningStyleBar';
import {
  styleConfig,
  styleBarColors,
} from './learningProfileHelpers';
import type { LearningProfile } from '@/types/learning';

interface Props {
  profile: LearningProfile | null;
  isLoading: boolean;
  hasAnalyzed: boolean;
}

export function LearningStyleCard({ profile, isLoading, hasAnalyzed }: Props) {
  const style = profile?.preferred_style;
  const config = style ? styleConfig[style] : null;
  const Icon = config?.icon;

  return (
    <Card className="border-border/50 shadow-sm">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Palette className="h-5 w-5 text-muted-foreground" />
          Learning Style
        </CardTitle>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            <Skeleton className="h-8 w-48" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        ) : !hasAnalyzed ? (
          <p className="text-sm text-muted-foreground">
            Run an analysis to discover your learning style
          </p>
        ) : config && Icon ? (
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Icon className={`h-8 w-8 ${config.color}`} />
              <div>
                <p className="text-lg font-semibold">{config.label}</p>
                <p className="text-xs text-muted-foreground">
                  {Math.round((profile?.style_confidence ?? 0) * 100)}%
                  confidence
                </p>
              </div>
            </div>

            {/* Style breakdown bars */}
            <div className="space-y-2">
              {Object.entries(styleConfig).map(([key, cfg], i) => {
                const breakdown = profile?.style_breakdown;
                const value = breakdown?.[key]
                  ? breakdown[key] * 100
                  : key === style
                    ? (profile?.style_confidence ?? 0) * 100
                    : 10;
                return (
                  <div key={key} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span>{cfg.label}</span>
                      <span className="text-muted-foreground">
                        {Math.round(value)}%
                      </span>
                    </div>
                    <LearningStyleBar
                      value={value}
                      color={styleBarColors[key]}
                      delay={i * 0.1}
                    />
                  </div>
                );
              })}
            </div>
          </div>
        ) : null}
      </CardContent>
    </Card>
  );
}

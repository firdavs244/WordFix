import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import {
  patternConfig,
} from './learningProfileHelpers';
import type { MistakePattern } from '@/types/learning';

interface Props {
  mistake: MistakePattern;
}

export function LearningMistakeItem({ mistake }: Props) {
  const config = patternConfig[mistake.type];

  return (
    <motion.div variants={staggerItem}>
      <Card className="border-border/50">
        <CardContent className="p-4">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <span className="font-medium">{mistake.description}</span>
                {config && (
                  <Badge
                    variant="outline"
                    className={`${config.bgColor} ${config.color}`}
                  >
                    {config.label}
                  </Badge>
                )}
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                {mistake.occurrence_count} occurrences
              </p>
            </div>
            {mistake.is_resolved && (
              <Badge variant="outline" className="border-green-300 text-green-600">
                Resolved
              </Badge>
            )}
          </div>

          {mistake.examples.length > 0 && (
            <div className="mt-3 space-y-1.5">
              {mistake.examples.slice(0, 2).map((ex, i) => (
                <div key={i} className="text-xs">
                  <span className="text-red-400 line-through">{ex.wrong}</span>
                  {' → '}
                  <span className="text-green-400">{ex.correct}</span>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

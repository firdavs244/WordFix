import { motion } from 'framer-motion';
import { staggerItem } from '@/lib/motion';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  reasonConfig,
} from './learningProfileHelpers';
import type { WordRecommendation } from '@/types/learning';

interface Props {
  recommendation: WordRecommendation;
  onAccept: (id: string) => void;
  isPending: boolean;
}

export function LearningRecommendationItem({
  recommendation,
  onAccept,
  isPending,
}: Props) {
  const config = reasonConfig[recommendation.reason_type];

  return (
    <motion.div variants={staggerItem}>
      <Card className="border-border/50">
        <CardContent className="flex items-center gap-3 p-4">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="font-semibold">{recommendation.word}</span>
              {config && (
                <Badge
                  variant="outline"
                  className={`${config.bgColor} ${config.color}`}
                >
                  {config.label}
                </Badge>
              )}
            </div>
            <p className="text-sm text-muted-foreground">
              {recommendation.translation}
            </p>
            <p className="mt-0.5 text-xs text-muted-foreground">
              {recommendation.reason}
            </p>
          </div>

          {recommendation.is_accepted ? (
            <CheckCircle2 className="h-5 w-5 shrink-0 text-green-500" />
          ) : (
            <Button
              size="sm"
              variant="outline"
              disabled={isPending}
              onClick={() => onAccept(recommendation.id)}
            >
              Add
            </Button>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

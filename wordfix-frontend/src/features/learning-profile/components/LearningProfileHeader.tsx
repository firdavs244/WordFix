import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import PageHeader from '@/components/shared/PageHeader';
import { formatTimeAgo } from './learningProfileHelpers';

interface Props {
  hasAnalyzed: boolean;
  lastAnalyzed: string | null;
  onAnalyze: () => void;
  isPending: boolean;
}

export function LearningProfileHeader({
  hasAnalyzed,
  lastAnalyzed,
  onAnalyze,
  isPending,
}: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >
      <PageHeader
        title="Learning Profile"
        description="AI-powered analysis of your learning patterns"
      />

      <div className="flex flex-col items-start gap-1 sm:items-end">
        <Button
          onClick={onAnalyze}
          disabled={isPending}
          size="lg"
          className="gap-2 shadow-lg shadow-primary/25"
        >
          {isPending ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Analyzing...
            </>
          ) : (
            <>
              <Sparkles className="h-5 w-5" />
              Analyze Profile
            </>
          )}
        </Button>
        {hasAnalyzed && lastAnalyzed && (
          <span className="text-xs text-muted-foreground">
            Last analyzed: {formatTimeAgo(lastAnalyzed)}
          </span>
        )}
      </div>
    </motion.div>
  );
}

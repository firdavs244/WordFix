import { motion } from 'framer-motion';
import { RotateCcw, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface DrillResultProps {
  correct: number;
  total: number;
  scorePct: number;
  onResolve: () => void;
  onRetry: () => void;
  onClose: () => void;
}

export function DrillResult({
  correct,
  total,
  scorePct,
  onResolve,
  onRetry,
  onClose,
}: DrillResultProps) {
  const getMessage = () => {
    if (scorePct === 100) return "Perfect! You've mastered this pair!";
    if (scorePct >= 80) return 'Great job! Almost there!';
    return "Keep practicing! You'll get it!";
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="space-y-6 text-center"
    >
      <Sparkles className="mx-auto h-12 w-12 text-primary" />
      <h2 className="font-heading text-2xl font-bold">🎉 Drill Complete!</h2>
      <p className="text-3xl font-bold">
        {correct}/{total}{' '}
        <span className="text-lg text-muted-foreground">({scorePct}%)</span>
      </p>
      <p className="text-muted-foreground">{getMessage()}</p>

      <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
        {scorePct >= 80 && (
          <Button onClick={onResolve} className="gap-2" size="lg">
            Mark as Resolved ✅
          </Button>
        )}
        <Button variant="outline" onClick={onRetry} className="gap-2" size="lg">
          <RotateCcw className="h-4 w-4" />
          Practice Again 🔄
        </Button>
        <Button variant="ghost" onClick={onClose} size="lg">
          Close
        </Button>
      </div>
    </motion.div>
  );
}

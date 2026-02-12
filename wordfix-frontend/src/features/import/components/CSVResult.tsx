import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Check, AlertCircle, ArrowRight, RotateCcw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router-dom';
import type { CSVImportResult } from '@/types/smart-import';

interface CSVResultProps {
  result: CSVImportResult;
  onReset: () => void;
}

export function CSVResult({ result, onReset }: CSVResultProps) {
  const navigate = useNavigate();
  const hasErrors = result.errors && result.errors.length > 0;

  // Confetti for 10+ imports
  useEffect(() => {
    if (result.imported < 10) return;
    const timer = setTimeout(async () => {
      try {
        const confetti = (await import('canvas-confetti')).default;
        confetti({ particleCount: 80, spread: 60, origin: { y: 0.6 } });
      } catch {
        // canvas-confetti not available
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [result.imported]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="space-y-6 text-center"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
        className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30"
      >
        <Check className="h-8 w-8 text-green-600 dark:text-green-400" />
      </motion.div>

      <div className="space-y-2">
        <h3 className="text-xl font-bold">CSV Import Complete!</h3>

        {/* Stats grid */}
        <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded-lg border bg-card p-3">
            <p className="text-2xl font-bold text-primary">{result.imported}</p>
            <p className="text-xs text-muted-foreground">Imported</p>
          </div>
          <div className="rounded-lg border bg-card p-3">
            <p className="text-2xl font-bold text-foreground">{result.total_in_file}</p>
            <p className="text-xs text-muted-foreground">In File</p>
          </div>
          <div className="rounded-lg border bg-card p-3">
            <p className="text-2xl font-bold text-yellow-500">{result.skipped_duplicate}</p>
            <p className="text-xs text-muted-foreground">Duplicates</p>
          </div>
          <div className="rounded-lg border bg-card p-3">
            <p className="text-2xl font-bold text-yellow-500">+{result.xp_earned}</p>
            <p className="text-xs text-muted-foreground">XP Earned</p>
          </div>
        </div>

        {result.categories_created.length > 0 && (
          <p className="text-sm text-muted-foreground">
            {result.categories_created.length} new {result.categories_created.length === 1 ? 'category' : 'categories'} created
          </p>
        )}
      </div>

      {/* Errors */}
      {hasErrors && (
        <div className="mx-auto max-w-md rounded-lg border border-destructive/30 bg-destructive/5 p-3 text-left">
          <div className="flex items-center gap-2 text-sm font-medium text-destructive">
            <AlertCircle className="h-4 w-4" />
            {result.errors!.length} row{result.errors!.length > 1 ? 's' : ''} skipped
          </div>
          <ul className="mt-1 space-y-0.5">
            {result.errors!.slice(0, 3).map((err, i) => (
              <li key={i} className="text-xs text-destructive/80">&bull; {err}</li>
            ))}
            {result.errors!.length > 3 && (
              <li className="text-xs text-muted-foreground">
                &hellip; and {result.errors!.length - 3} more
              </li>
            )}
          </ul>
        </div>
      )}

      {/* Actions */}
      <div className="flex justify-center gap-3 pt-2">
        <Button variant="outline" onClick={onReset}>
          <RotateCcw className="mr-2 h-4 w-4" />
          Import Another
        </Button>
        <Button onClick={() => navigate('/words')}>
          View My Words
          <ArrowRight className="ml-2 h-4 w-4" />
        </Button>
      </div>
    </motion.div>
  );
}

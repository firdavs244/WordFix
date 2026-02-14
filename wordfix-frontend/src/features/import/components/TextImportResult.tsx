import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

interface TextImportResultProps {
  created: number;
  skipped: number;
  onReset: () => void;
  onViewWords: () => void;
}

export function TextImportResult({ created, skipped, onReset, onViewWords }: TextImportResultProps) {
  return (
    <motion.div
      key="result"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
    >
      <Card className="text-center">
        <CardContent className="space-y-6 py-12">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
            className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30"
          >
            <Check className="h-10 w-10 text-green-600 dark:text-green-400" />
          </motion.div>
          <div>
            <h2 className="text-2xl font-bold text-foreground">Import Complete!</h2>
            <p className="mt-2 text-muted-foreground">
              Successfully added <strong>{created}</strong> new words to your vocabulary
            </p>
            {skipped > 0 && (
              <p className="text-sm text-muted-foreground">
                {skipped} words were skipped (already in your vocabulary)
              </p>
            )}
          </div>
          <div className="flex justify-center gap-3">
            <Button variant="outline" onClick={onReset}>
              Import More
            </Button>
            <Button onClick={onViewWords}>View My Words</Button>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}

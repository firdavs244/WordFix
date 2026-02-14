import { motion } from 'framer-motion';
import { Sparkles, Upload, ArrowLeft, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import type { WordSuggestion } from '@/types';
import { difficultyColor } from './importHelpers';

interface TextImportReviewProps {
  suggestions: WordSuggestion[];
  onToggleWord: (index: number) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onImport: () => void;
  onBack: () => void;
  selectedCount: number;
  isImporting: boolean;
}

export function TextImportReview({
  suggestions,
  onToggleWord,
  onSelectAll,
  onDeselectAll,
  onImport,
  onBack,
  selectedCount,
  isImporting,
}: TextImportReviewProps) {
  return (
    <motion.div
      key="review"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-4"
    >
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-primary" />
                Found {suggestions.length} Words
              </CardTitle>
              <CardDescription>
                Select the words you want to add to your vocabulary
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={onSelectAll}>
                Select All
              </Button>
              <Button variant="outline" size="sm" onClick={onDeselectAll}>
                Deselect All
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {suggestions.map((suggestion, index) => (
              <motion.div
                key={suggestion.word}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                className={`flex items-start gap-3 rounded-lg border p-4 transition-colors ${
                  suggestion.selected
                    ? 'border-primary/30 bg-primary/5'
                    : 'border-border bg-card opacity-60'
                }`}
              >
                <Checkbox
                  checked={suggestion.selected}
                  onCheckedChange={() => onToggleWord(index)}
                  className="mt-1"
                />
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-foreground">{suggestion.word}</span>
                    <span className="text-muted-foreground">—</span>
                    <span className="text-muted-foreground">{suggestion.translation}</span>
                    <Badge variant="outline" className={difficultyColor(suggestion.difficulty)}>
                      {suggestion.difficulty}
                    </Badge>
                    {suggestion.part_of_speech && (
                      <Badge variant="secondary">{suggestion.part_of_speech}</Badge>
                    )}
                  </div>
                  {suggestion.context_sentence && (
                    <p className="text-sm italic text-muted-foreground">
                      &ldquo;{suggestion.context_sentence}&rdquo;
                    </p>
                  )}
                  {suggestion.reason && (
                    <p className="text-xs text-muted-foreground">{suggestion.reason}</p>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="flex items-center justify-between">
        <Button variant="outline" onClick={onBack}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        <Button onClick={onImport} disabled={selectedCount === 0 || isImporting} size="lg">
          {isImporting ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Importing...
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Import {selectedCount} Words
            </>
          )}
        </Button>
      </div>
    </motion.div>
  );
}

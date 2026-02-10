import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, Sparkles, Upload, Check, Loader2, ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Checkbox } from '@/components/ui/checkbox';
import { useAnalyzeText, useImportWords } from '../hooks/useImport';
import type { WordSuggestion } from '@/types';

type ImportStep = 'input' | 'review' | 'result';

export function ImportPage() {
  const [step, setStep] = useState<ImportStep>('input');
  const [text, setText] = useState('');
  const [suggestions, setSuggestions] = useState<WordSuggestion[]>([]);
  const [importResult, setImportResult] = useState<{ created: number; skipped: number } | null>(null);

  const analyzeText = useAnalyzeText();
  const importWords = useImportWords();

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    const result = await analyzeText.mutateAsync({ text, max_words: 20 });
    const withSelection = result.data.suggestions.map((s) => ({ ...s, selected: true }));
    setSuggestions(withSelection);
    setStep('review');
  };

  const toggleWord = (index: number) => {
    setSuggestions((prev) =>
      prev.map((s, i) => (i === index ? { ...s, selected: !s.selected } : s)),
    );
  };

  const selectAll = () => {
    setSuggestions((prev) => prev.map((s) => ({ ...s, selected: true })));
  };

  const deselectAll = () => {
    setSuggestions((prev) => prev.map((s) => ({ ...s, selected: false })));
  };

  const handleImport = async () => {
    const selected = suggestions.filter((s) => s.selected);
    if (selected.length === 0) return;

    const result = await importWords.mutateAsync({
      words: selected.map((s) => ({
        original_word: s.word,
        translation: s.translation,
        part_of_speech: s.part_of_speech,
        difficulty_level: s.difficulty,
        context_sentence: s.context_sentence,
      })),
    });
    setImportResult({ created: result.data.created, skipped: result.data.skipped });
    setStep('result');
  };

  const reset = () => {
    setText('');
    setSuggestions([]);
    setImportResult(null);
    setStep('input');
  };

  const selectedCount = suggestions.filter((s) => s.selected).length;

  const difficultyColor = (d: string) => {
    switch (d) {
      case 'easy': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
      case 'medium': return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'hard': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
      default: return '';
    }
  };

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="font-heading text-3xl font-bold text-foreground">Smart Import</h1>
        <p className="mt-1 text-muted-foreground">
          Paste any English text and AI will find words for you to learn
        </p>
      </motion.div>

      {/* Steps indicator */}
      <div className="flex items-center gap-2">
        {['Input Text', 'Review Words', 'Done'].map((label, i) => {
          const active = i === ['input', 'review', 'result'].indexOf(step);
          const done = ['input', 'review', 'result'].indexOf(step) > i;
          return (
            <div key={label} className="flex items-center gap-2">
              <div
                className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium transition-colors ${
                  active
                    ? 'bg-primary text-primary-foreground'
                    : done
                      ? 'bg-green-500 text-white'
                      : 'bg-muted text-muted-foreground'
                }`}
              >
                {done ? <Check className="h-4 w-4" /> : i + 1}
              </div>
              <span className={`text-sm ${active ? 'font-medium text-foreground' : 'text-muted-foreground'}`}>
                {label}
              </span>
              {i < 2 && <div className="mx-2 h-px w-8 bg-border" />}
            </div>
          );
        })}
      </div>

      <AnimatePresence mode="wait">
        {/* Step 1: Input */}
        {step === 'input' && (
          <motion.div
            key="input"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-primary" />
                  Paste Your Text
                </CardTitle>
                <CardDescription>
                  Paste an article, essay, book excerpt, or any English text (max 5000 characters)
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Paste your English text here..."
                  className="min-h-[200px] resize-y"
                  maxLength={5000}
                />
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">
                    {text.length} / 5000 characters
                  </span>
                  <Button
                    onClick={handleAnalyze}
                    disabled={!text.trim() || analyzeText.isPending}
                    size="lg"
                  >
                    {analyzeText.isPending ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Sparkles className="mr-2 h-4 w-4" />
                        Analyze Text
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Step 2: Review */}
        {step === 'review' && (
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
                    <Button variant="outline" size="sm" onClick={selectAll}>
                      Select All
                    </Button>
                    <Button variant="outline" size="sm" onClick={deselectAll}>
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
                        onCheckedChange={() => toggleWord(index)}
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
              <Button variant="outline" onClick={() => setStep('input')}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>
              <Button
                onClick={handleImport}
                disabled={selectedCount === 0 || importWords.isPending}
                size="lg"
              >
                {importWords.isPending ? (
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
        )}

        {/* Step 3: Result */}
        {step === 'result' && importResult && (
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
                    Successfully added <strong>{importResult.created}</strong> new words to your vocabulary
                  </p>
                  {importResult.skipped > 0 && (
                    <p className="text-sm text-muted-foreground">
                      {importResult.skipped} words were skipped (already in your vocabulary)
                    </p>
                  )}
                </div>
                <div className="flex justify-center gap-3">
                  <Button variant="outline" onClick={reset}>
                    Import More
                  </Button>
                  <Button onClick={() => (window.location.href = '/words')}>
                    View My Words
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

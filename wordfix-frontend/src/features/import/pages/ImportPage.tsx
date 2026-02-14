import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, Sparkles, Upload, Check, Loader2 } from 'lucide-react';
import * as Tabs from '@radix-ui/react-tabs';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { useAnalyzeText, useImportWords, useValidateCSV, useImportCSV } from '../hooks/useImport';
import { CSVDropZone } from '../components/CSVDropZone';
import { CSVPreview } from '../components/CSVPreview';
import { CSVResult } from '../components/CSVResult';
import { TextImportReview } from '../components/TextImportReview';
import { TextImportResult } from '../components/TextImportResult';
import type { ImportStep } from '../components/importHelpers';
import type { WordSuggestion } from '@/types';
import type { CSVValidateResult, CSVImportResult } from '@/types/smart-import';

export function ImportPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState<ImportStep>('input');
  const [text, setText] = useState('');
  const [suggestions, setSuggestions] = useState<WordSuggestion[]>([]);
  const [importResult, setImportResult] = useState<{ created: number; skipped: number } | null>(
    null,
  );

  const analyzeText = useAnalyzeText();
  const importWords = useImportWords();

  // CSV state
  const [csvStep, setCsvStep] = useState<'upload' | 'preview' | 'result'>('upload');
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [csvValidation, setCsvValidation] = useState<CSVValidateResult | null>(null);
  const [csvResult, setCsvResult] = useState<CSVImportResult | null>(null);
  const validateCSV = useValidateCSV();
  const importCSV = useImportCSV();

  // ─── Handlers ────────────────────────────────────────────────────────────────

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

  const selectAll = () => setSuggestions((prev) => prev.map((s) => ({ ...s, selected: true })));
  const deselectAll = () =>
    setSuggestions((prev) => prev.map((s) => ({ ...s, selected: false })));

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

  const handleCSVValidate = async (file: File) => {
    setCsvFile(file);
    const result = await validateCSV.mutateAsync(file);
    setCsvValidation(result.data);
    setCsvStep('preview');
  };

  const handleCSVImport = async () => {
    if (!csvFile) return;
    const result = await importCSV.mutateAsync(csvFile);
    setCsvResult(result.data);
    setCsvStep('result');
  };

  const resetCSV = () => {
    setCsvFile(null);
    setCsvValidation(null);
    setCsvResult(null);
    setCsvStep('upload');
  };

  const selectedCount = suggestions.filter((s) => s.selected).length;

  // ─── Render ──────────────────────────────────────────────────────────────────

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="font-heading text-3xl font-bold text-foreground">Smart Import</h1>
        <p className="mt-1 text-muted-foreground">
          Import words from text or CSV to build your vocabulary
        </p>
      </motion.div>

      <Tabs.Root defaultValue="text" className="space-y-6">
        <Tabs.List className="inline-flex h-10 items-center justify-start rounded-md bg-muted p-1 text-muted-foreground">
          <Tabs.Trigger
            value="text"
            className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm"
          >
            <FileText className="h-4 w-4" />
            Text Import
          </Tabs.Trigger>
          <Tabs.Trigger
            value="csv"
            className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm"
          >
            <Upload className="h-4 w-4" />
            CSV Import
          </Tabs.Trigger>
        </Tabs.List>

        {/* ─── Text Import Tab ────────────────────────────────────────────── */}
        <Tabs.Content value="text" className="space-y-6">
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
                  <span
                    className={`text-sm ${active ? 'font-medium text-foreground' : 'text-muted-foreground'}`}
                  >
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
                      Paste an article, essay, book excerpt, or any English text (max 5000
                      characters)
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
              <TextImportReview
                suggestions={suggestions}
                onToggleWord={toggleWord}
                onSelectAll={selectAll}
                onDeselectAll={deselectAll}
                onImport={handleImport}
                onBack={() => setStep('input')}
                selectedCount={selectedCount}
                isImporting={importWords.isPending}
              />
            )}

            {/* Step 3: Result */}
            {step === 'result' && importResult && (
              <TextImportResult
                created={importResult.created}
                skipped={importResult.skipped}
                onReset={reset}
                onViewWords={() => navigate('/words')}
              />
            )}
          </AnimatePresence>
        </Tabs.Content>

        {/* ─── CSV Import Tab ─────────────────────────────────────────────── */}
        <Tabs.Content value="csv" className="space-y-6">
          <AnimatePresence mode="wait">
            {csvStep === 'upload' && (
              <motion.div
                key="csv-upload"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Upload className="h-5 w-5 text-primary" />
                      Upload CSV File
                    </CardTitle>
                    <CardDescription>
                      Upload a CSV file with columns: word (required), translation,
                      difficulty_level, category
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <CSVDropZone onFileSelect={handleCSVValidate} isLoading={validateCSV.isPending} />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {csvStep === 'preview' && csvValidation && csvFile && (
              <motion.div
                key="csv-preview"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-primary" />
                      Preview & Import
                    </CardTitle>
                    <CardDescription>Review the parsed data before importing</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <CSVPreview
                      result={csvValidation}
                      file={csvFile}
                      onImport={handleCSVImport}
                      onCancel={resetCSV}
                      isImporting={importCSV.isPending}
                    />
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {csvStep === 'result' && csvResult && (
              <motion.div
                key="csv-result"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <Card>
                  <CardContent className="py-8">
                    <CSVResult result={csvResult} onReset={resetCSV} />
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>
        </Tabs.Content>
      </Tabs.Root>
    </div>
  );
}

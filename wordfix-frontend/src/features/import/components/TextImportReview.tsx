import { Loader2, Library, AlertCircle, Sparkles, ListChecks } from 'lucide-react';
import TextImportWordRow from './TextImportWordRow';
import type { WordSuggestion } from '@/types';
import { cn } from '@/lib/utils';

interface TextImportReviewProps {
  words: WordSuggestion[];
  filteredWords: WordSuggestion[];
  selectedIds: Set<number>;
  onToggle: (index: number) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onSelectAllNew?: () => void;
  onImport: () => void;
  isImporting: boolean;
  parseMode: string;
  textDifficulty: string;
  alreadyInLibrary: number;
  newWords?: number;
  skippedNonEnglish?: number;
  aiUsed?: boolean;
  levelFilter: string;
  onLevelFilterChange: (f: string) => void;
  showOnlyNew?: boolean;
  onShowOnlyNewChange?: (v: boolean) => void;
}

const LEVEL_FILTERS = [
  { value: 'all', label: 'All' },
  { value: 'A', label: 'A1-A2' },
  { value: 'B', label: 'B1-B2' },
  { value: 'C', label: 'C1-C2' },
];

const parseModeLabels: Record<string, { label: string; icon: string }> = {
  ai: { label: 'AI Analyzed', icon: '🤖' },
  structured: { label: 'Pattern Matched', icon: '📋' },
  ai_extracted: { label: 'AI Extracted', icon: '🤖' },
  plain_english: { label: 'English text analyzed', icon: '📝' },
  mixed: { label: 'Mixed content parsed', icon: '🔀' },
  fallback: { label: 'Basic Extract', icon: '⚠️' },
};

export default function TextImportReview({
  words, filteredWords, selectedIds, onToggle, onSelectAll, onDeselectAll,
  onSelectAllNew, onImport, isImporting, parseMode, textDifficulty, alreadyInLibrary,
  newWords, skippedNonEnglish, aiUsed, levelFilter, onLevelFilterChange,
  showOnlyNew, onShowOnlyNewChange,
}: TextImportReviewProps) {
  const modeInfo = parseModeLabels[parseMode] || { label: parseMode, icon: '📄' };
  return (
    <div className="overflow-hidden rounded-2xl border border-border/50 shadow-card">
      {/* Header with stats */}
      <div className="border-b border-border/30 bg-muted/20 px-5 py-4 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <span className="font-heading text-sm font-semibold">Found {words.length} words</span>
            {parseMode && (
              <span className="ml-2 inline-flex items-center gap-1 text-[10px] text-muted-foreground">
                {modeInfo.icon} {modeInfo.label}
              </span>
            )}
            {aiUsed && (
              <span className="ml-1.5 inline-flex items-center gap-0.5 rounded-full bg-violet-100 px-1.5 py-0.5 text-[9px] font-medium text-violet-600 dark:bg-violet-900/30 dark:text-violet-400">
                <Sparkles className="h-2.5 w-2.5" />
                AI
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button onClick={onSelectAll} className="text-xs text-muted-foreground hover:text-foreground">Select All</button>
            {onSelectAllNew && (
              <button onClick={onSelectAllNew} className="flex items-center gap-1 text-xs text-primary hover:text-primary/80">
                <ListChecks className="h-3 w-3" /> Only New
              </button>
            )}
            <button onClick={onDeselectAll} className="text-xs text-muted-foreground hover:text-foreground">Deselect All</button>
            <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs text-primary">{selectedIds.size} selected</span>
          </div>
        </div>

        {/* Info badges */}
        <div className="flex flex-wrap items-center gap-2">
          {textDifficulty && (
            <span className="rounded-full bg-blue-100 px-2.5 py-0.5 text-[10px] font-medium text-blue-600 dark:bg-blue-900/30 dark:text-blue-400">
              Text level: {textDifficulty}
            </span>
          )}
          {(newWords ?? 0) > 0 && (
            <span className="rounded-full bg-emerald-100 px-2.5 py-0.5 text-[10px] font-medium text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400">
              {newWords} new words
            </span>
          )}
          {alreadyInLibrary > 0 && (
            <span className="flex items-center gap-1 rounded-full bg-amber-100 px-2.5 py-0.5 text-[10px] font-medium text-amber-600 dark:bg-amber-900/30 dark:text-amber-400">
              <Library className="h-3 w-3" />
              {alreadyInLibrary} already in library
            </span>
          )}
          {(skippedNonEnglish ?? 0) > 0 && (
            <span className="flex items-center gap-1 rounded-full bg-purple-100 px-2.5 py-0.5 text-[10px] font-medium text-purple-600 dark:bg-purple-900/30 dark:text-purple-400">
              <AlertCircle className="h-3 w-3" />
              {skippedNonEnglish} non-English filtered
            </span>
          )}
        </div>

        {/* Filter controls */}
        <div className="flex items-center gap-3">
          <div className="flex gap-1.5">
            {LEVEL_FILTERS.map((f) => (
              <button
                key={f.value}
                onClick={() => onLevelFilterChange(f.value)}
                className={cn(
                  'rounded-full px-3 py-1 text-[11px] font-medium transition-colors',
                  levelFilter === f.value
                    ? 'bg-primary text-white'
                    : 'bg-muted/40 text-muted-foreground hover:bg-muted/60',
                )}
              >
                {f.label}
              </button>
            ))}
          </div>
          {onShowOnlyNewChange && (
            <button
              onClick={() => onShowOnlyNewChange(!showOnlyNew)}
              className={cn(
                'rounded-full px-3 py-1 text-[11px] font-medium transition-colors',
                showOnlyNew
                  ? 'bg-emerald-500 text-white'
                  : 'bg-muted/40 text-muted-foreground hover:bg-muted/60',
              )}
            >
              New only
            </button>
          )}
        </div>
      </div>

      {/* Word list */}
      <div className="max-h-[400px] divide-y divide-border/20 overflow-y-auto scrollbar-thin">
        {filteredWords.map((w) => {
          // Find the original index in the full suggestions array
          const originalIndex = words.indexOf(w);
          return (
            <TextImportWordRow key={originalIndex} word={w} isSelected={selectedIds.has(originalIndex)} onToggle={() => onToggle(originalIndex)} />
          );
        })}
        {filteredWords.length === 0 && (
          <div className="px-5 py-8 text-center text-sm text-muted-foreground">
            No words match this level filter
          </div>
        )}
      </div>
      <div className="sticky bottom-0 border-t border-border/30 bg-card px-5 py-4">
        <button
          onClick={onImport}
          disabled={selectedIds.size === 0 || isImporting}
          className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-semibold text-white transition-all disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isImporting ? <><Loader2 className="h-4 w-4 animate-spin" /> Importing...</> : `Import ${selectedIds.size} Words`}
        </button>
      </div>
    </div>
  );
}

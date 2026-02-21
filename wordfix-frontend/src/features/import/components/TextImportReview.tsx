import { Loader2 } from 'lucide-react';
import TextImportWordRow from './TextImportWordRow';
import type { WordSuggestion } from '@/types';

interface TextImportReviewProps {
  words: WordSuggestion[];
  selectedIds: Set<number>;
  onToggle: (index: number) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onImport: () => void;
  isImporting: boolean;
}

export default function TextImportReview({ words, selectedIds, onToggle, onSelectAll, onDeselectAll, onImport, isImporting }: TextImportReviewProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border/50 shadow-card">
      <div className="flex items-center justify-between border-b border-border/30 bg-muted/20 px-5 py-4">
        <span className="font-heading text-sm font-semibold">Found {words.length} words</span>
        <div className="flex items-center gap-2">
          <button onClick={onSelectAll} className="text-xs text-muted-foreground hover:text-foreground">Select All</button>
          <button onClick={onDeselectAll} className="text-xs text-muted-foreground hover:text-foreground">Deselect All</button>
          <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs text-primary">{selectedIds.size} selected</span>
        </div>
      </div>
      <div className="max-h-[400px] divide-y divide-border/20 overflow-y-auto scrollbar-thin">
        {words.map((w, i) => (
          <TextImportWordRow key={i} word={w} isSelected={selectedIds.has(i)} onToggle={() => onToggle(i)} />
        ))}
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

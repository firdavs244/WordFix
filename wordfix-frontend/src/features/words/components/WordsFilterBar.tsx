import { Search, X } from 'lucide-react';
import WordsSegmentedControl from './WordsSegmentedControl';
import WordsViewToggle from './WordsViewToggle';
import type { WordsFiltersState } from '../WordsPage';

interface Props {
  filters: WordsFiltersState;
  onFiltersChange: (f: WordsFiltersState) => void;
  view: 'grid' | 'list';
  onViewChange: (v: 'grid' | 'list') => void;
}

const difficultyOptions = [
  { value: 'all', label: 'All' },
  { value: 'easy', label: 'Easy' },
  { value: 'medium', label: 'Medium' },
  { value: 'hard', label: 'Hard' },
];

export default function WordsFilterBar({ filters, onFiltersChange, view, onViewChange }: Props) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      {/* Search */}
      <div className="relative w-full sm:w-72">
        <Search className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground/40" />
        <input
          type="text"
          placeholder="Search words..."
          value={filters.search}
          onChange={(e) => onFiltersChange({ ...filters, search: e.target.value, page: 1 })}
          className="h-10 w-full rounded-xl border border-border/50 bg-card pl-10 pr-10 text-sm placeholder:text-muted-foreground/40 transition-all focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
        />
        {filters.search.length > 0 && (
          <button
            onClick={() => onFiltersChange({ ...filters, search: '', page: 1 })}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition-opacity hover:text-foreground"
            aria-label="Clear search"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {/* Right controls */}
      <div className="flex items-center gap-2 sm:ml-auto">
        <WordsSegmentedControl
          options={difficultyOptions}
          value={filters.difficulty}
          onChange={(v) => onFiltersChange({ ...filters, difficulty: v as WordsFiltersState['difficulty'], page: 1 })}
        />
        <WordsViewToggle view={view} onChange={onViewChange} />
      </div>
    </div>
  );
}

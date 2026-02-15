import { useState } from 'react';
import { PageTransition } from '@/components/shared';
import WordsHeader from './components/WordsHeader';
import WordsStatsBar from './components/WordsStatsBar';
import WordsFilterBar from './components/WordsFilterBar';
import WordsGrid from './components/WordsGrid';
import WordsList from './components/WordsList';
import type { DifficultyLevel } from '@/types';

export interface WordsFiltersState {
  search: string;
  difficulty: DifficultyLevel | 'all';
  page: number;
}

export default function WordsPage() {
  const [view, setView] = useState<'grid' | 'list'>('grid');
  const [filters, setFilters] = useState<WordsFiltersState>({
    search: '',
    difficulty: 'all',
    page: 1,
  });

  return (
    <PageTransition>
      <div className="space-y-6">
        <WordsHeader />
        <WordsStatsBar />
        <WordsFilterBar filters={filters} onFiltersChange={setFilters} view={view} onViewChange={setView} />
        {view === 'grid' ? <WordsGrid filters={filters} /> : <WordsList filters={filters} />}
      </div>
    </PageTransition>
  );
}

import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { EmptyState } from '@/components/shared';
import WordListItem from './WordListItem';
import WordsPagination from './WordsPagination';
import { useWords, useDeleteWord } from '../hooks/useWords';
import { useDebounce } from '@/hooks/useDebounce';
import type { WordsFiltersState } from '../WordsPage';

interface Props {
  filters: WordsFiltersState;
}

export default function WordsList({ filters }: Props) {
  const debouncedSearch = useDebounce(filters.search, 300);
  const { data, isLoading } = useWords({
    search: debouncedSearch || undefined,
    difficulty_level: filters.difficulty === 'all' ? undefined : filters.difficulty,
    page: filters.page,
    page_size: 20,
    ordering: '-created_at',
  });
  const deleteWord = useDeleteWord();
  const words = data?.data ?? [];
  const meta = data?.meta;

  if (isLoading) {
    return (
      <div className="space-y-2">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="h-14 animate-pulse rounded-xl bg-muted" />
        ))}
      </div>
    );
  }

  if (words.length === 0) {
    return <EmptyState icon={Search} title="No words found" description="Try adjusting your search or filters" />;
  }

  return (
    <>
      <div className="overflow-hidden rounded-2xl border border-border/50 bg-card shadow-card">
        <div className="grid grid-cols-12 bg-muted/30 px-5 py-3">
          <span className="col-span-4 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Word</span>
          <span className="col-span-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Translation</span>
          <span className="col-span-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Difficulty</span>
          <span className="col-span-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Category</span>
          <span className="col-span-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Actions</span>
        </div>
        <motion.div variants={staggerContainer} initial="initial" animate="animate" className="divide-y divide-border/30">
          {words.map((word) => (
            <WordListItem key={word.id} word={word} onDelete={(id) => deleteWord.mutate(id)} />
          ))}
        </motion.div>
      </div>
      {meta && meta.total_pages > 1 && (
        <WordsPagination currentPage={meta.page} totalPages={meta.total_pages} onPageChange={(p) => void p} />
      )}
    </>
  );
}

import { motion } from 'framer-motion';
import { Search } from 'lucide-react';
import { staggerContainer, staggerItem } from '@/lib/motion';
import { EmptyState } from '@/components/shared';
import WordCard from './WordCard';
import WordsPagination from './WordsPagination';
import { useWords, useDeleteWord } from '../hooks/useWords';
import { useDebounce } from '@/hooks/useDebounce';
import type { WordsFiltersState } from '../WordsPage';

interface Props {
  filters: WordsFiltersState;
}

export default function WordsGrid({ filters }: Props) {
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
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="h-48 animate-pulse rounded-2xl bg-muted" />
        ))}
      </div>
    );
  }

  if (words.length === 0) {
    return <EmptyState icon={Search} title="No words found" description="Try adjusting your search or filters" />;
  }

  return (
    <>
      <motion.div variants={staggerContainer} initial="initial" animate="animate" className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {words.map((word) => (
          <motion.div key={word.id} variants={staggerItem}>
            <WordCard word={word} onDelete={(id) => deleteWord.mutate(id)} />
          </motion.div>
        ))}
      </motion.div>
      {meta && meta.total_pages > 1 && (
        <WordsPagination currentPage={meta.page} totalPages={meta.total_pages} onPageChange={(p) => void p} />
      )}
    </>
  );
}

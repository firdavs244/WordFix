import { useState } from 'react';
import { motion } from 'framer-motion';
import { Archive, ArchiveRestore, Search, X } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { EmptyState } from '@/components/common/EmptyState';
import { EnrichmentStatusBadge } from './EnrichmentStatusBadge';
import { useArchivedWords, useUnarchiveWord } from '../hooks/useWords';
import { listContainerVariants, listItemVariants, cardHoverVariants } from '@/components/animations/PageTransition';
import type { Word, DifficultyLevel } from '@/types';

const difficultyConfig: Record<DifficultyLevel, { label: string; variant: 'success' | 'warning' | 'destructive' }> = {
  easy: { label: 'Easy', variant: 'success' },
  medium: { label: 'Medium', variant: 'warning' },
  hard: { label: 'Hard', variant: 'destructive' },
};

interface ArchivedWordsSectionProps {
  onWordClick?: (word: Word) => void;
}

export function ArchivedWordsSection({ onWordClick }: ArchivedWordsSectionProps) {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const { data, isLoading } = useArchivedWords({ page, page_size: 20 });
  const unarchiveWord = useUnarchiveWord();

  const allWords: Word[] = data?.data ?? [];
  const meta = data?.meta;
  const words = search
    ? allWords.filter((w) =>
        w.original_word.toLowerCase().includes(search.toLowerCase()) ||
        w.translation.toLowerCase().includes(search.toLowerCase())
      )
    : allWords;

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search archived words..."
          className="pl-9"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        {search && (
          <button onClick={() => setSearch('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground">
            <X className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Loading */}
      {isLoading && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i} className="border-border/50">
              <CardContent className="p-4 space-y-2">
                <Skeleton className="h-5 w-2/3" />
                <Skeleton className="h-4 w-1/2" />
                <Skeleton className="h-3 w-full" />
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Empty */}
      {!isLoading && words.length === 0 && (
        <EmptyState
          icon={Archive}
          title={search ? 'No matches' : 'No archived words'}
          description={search ? 'Try a different search term.' : 'Words you archive will appear here.'}
        />
      )}

      {/* Words grid */}
      {!isLoading && words.length > 0 && (
        <motion.div
          className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3"
          variants={listContainerVariants}
          initial="hidden"
          animate="show"
        >
          {words.map((word) => {
            const dc = difficultyConfig[word.difficulty_level as DifficultyLevel] || difficultyConfig.medium;
            return (
              <motion.div key={word.id} variants={listItemVariants}>
                <motion.div variants={cardHoverVariants} initial="rest" whileHover="hover" whileTap="tap">
                  <Card
                    className="cursor-pointer border-border/50 overflow-hidden group relative"
                    onClick={() => onWordClick?.(word)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <h3 className="font-heading text-base font-semibold truncate">{word.original_word}</h3>
                          <p className="text-sm text-muted-foreground truncate mt-0.5">{word.translation}</p>
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-8 w-8 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity"
                          onClick={(e) => { e.stopPropagation(); unarchiveWord.mutate(word.id); }}
                          title="Unarchive"
                        >
                          <ArchiveRestore className="h-4 w-4 text-primary" />
                        </Button>
                      </div>
                      <div className="mt-2 flex flex-wrap gap-1">
                        <Badge variant={dc.variant} className="text-[10px]">{dc.label}</Badge>
                        {word.part_of_speech && <Badge variant="outline" className="text-[10px]">{word.part_of_speech}</Badge>}
                        <EnrichmentStatusBadge status={word.enrichment_status} showLabel={false} />
                      </div>
                      {word.archived_at && (
                        <p className="mt-2 text-[10px] text-muted-foreground">
                          Archived {new Date(word.archived_at).toLocaleDateString()}
                        </p>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              </motion.div>
            );
          })}
        </motion.div>
      )}

      {/* Pagination */}
      {meta && meta.total_pages > 1 && (
        <div className="flex items-center justify-center gap-2 pt-2">
          <Button variant="outline" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            Previous
          </Button>
          <span className="text-sm text-muted-foreground">Page {meta.page} of {meta.total_pages}</span>
          <Button variant="outline" size="sm" disabled={page >= meta.total_pages} onClick={() => setPage((p) => p + 1)}>
            Next
          </Button>
        </div>
      )}
    </div>
  );
}

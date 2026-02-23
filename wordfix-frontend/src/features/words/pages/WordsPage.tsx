import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BookOpen,
  Grid3X3,
  List,
  Plus,
  Search,
  Trash2,
  X,
  Check,
  Archive,
  Sparkles,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { EmptyState } from '@/components/common/EmptyState';
import { PageTransition } from '@/components/animations/PageTransition';
import { listContainerVariants, listItemVariants, cardHoverVariants } from '@/components/animations/PageTransition';
import { useWords, useDeleteWord, useWordStats, useArchiveWord, useEnrichAll } from '../hooks/useWords';
import AddWordModal from '../components/AddWordModal';
import { WordDetailModal } from '../components/WordDetailModal';
import { EnrichmentStatusBadge } from '../components/EnrichmentStatusBadge';
import { ArchiveButton } from '../components/ArchiveButton';
import { ArchivedWordsSection } from '../components/ArchivedWordsSection';
import type { DifficultyLevel, WordFilters, Word } from '@/types';
import { Skeleton } from '@/components/ui/skeleton';
import { cn } from '@/lib/utils';

const difficultyConfig = {
  easy: { label: 'Easy', variant: 'success' as const, color: 'bg-success/10 text-success' },
  medium: { label: 'Medium', variant: 'warning' as const, color: 'bg-warning/10 text-warning-foreground' },
  hard: { label: 'Hard', variant: 'destructive' as const, color: 'bg-error/10 text-error' },
};

export function WordsPage() {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<DifficultyLevel | ''>('');
  const [showAddModal, setShowAddModal] = useState(false);
  const [page, setPage] = useState(1);
  const [activeTab, setActiveTab] = useState<'active' | 'archived'>('active');
  const [selectedWord, setSelectedWord] = useState<Word | null>(null);

  const filters: WordFilters = useMemo(() => ({
    search: searchQuery || undefined,
    difficulty_level: selectedDifficulty || undefined,
    page,
    page_size: 20,
    ordering: '-created_at',
  }), [searchQuery, selectedDifficulty, page]);

  const { data: wordsData, isLoading } = useWords(filters);
  const { data: statsData } = useWordStats();
  const deleteWord = useDeleteWord();
  const archiveWord = useArchiveWord();
  const enrichAll = useEnrichAll();

  const words = wordsData?.data ?? [];
  const meta = wordsData?.meta;
  const stats = statsData?.data;

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this word?')) {
      deleteWord.mutate(id);
    }
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-6xl space-y-6">
        {/* Header */}
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="font-heading text-3xl font-bold">Word Bank</h1>
            <p className="mt-1 text-muted-foreground">
              {stats ? `${stats.total} words · ${stats.mastered} mastered` : 'Manage your vocabulary'}
            </p>
          </div>
          <Button className="gap-2 shadow-lg shadow-primary/25" onClick={() => setShowAddModal(true)}>
            <Plus className="h-5 w-5" />
            Add Word
          </Button>
        </div>

        {/* Tab switcher: Active / Archived */}
        <div className="flex items-center gap-1 rounded-lg border border-border bg-muted/30 p-1 w-fit">
          <button
            onClick={() => setActiveTab('active')}
            className={cn(
              'flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium transition-all',
              activeTab === 'active' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <BookOpen className="h-4 w-4" />
            Active
          </button>
          <button
            onClick={() => setActiveTab('archived')}
            className={cn(
              'flex items-center gap-1.5 rounded-md px-4 py-2 text-sm font-medium transition-all',
              activeTab === 'archived' ? 'bg-background text-foreground shadow-sm' : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <Archive className="h-4 w-4" />
            Archived
          </button>
        </div>

        {/* Archived tab */}
        {activeTab === 'archived' && (
          <ArchivedWordsSection onWordClick={setSelectedWord} />
        )}

        {/* Active tab content */}
        {activeTab === 'active' && (
        <>
        {/* Stats Cards */}
        {stats && stats.total > 0 && (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: 'Total', value: stats.total, color: 'text-primary' },
              { label: 'Mastered', value: stats.mastered, color: 'text-success' },
              { label: 'Learning', value: stats.learning, color: 'text-warning-foreground' },
              { label: 'New', value: stats.new, color: 'text-muted-foreground' },
            ].map((s) => (
              <Card key={s.label} className="border-border/50">
                <CardContent className="p-4 text-center">
                  <p className={`font-heading text-2xl font-bold ${s.color}`}>{s.value}</p>
                  <p className="text-xs text-muted-foreground">{s.label}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Search & Filters */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search words..."
              className="pl-9"
              value={searchQuery}
              onChange={(e) => { setSearchQuery(e.target.value); setPage(1); }}
            />
            {searchQuery && (
              <button
                onClick={() => { setSearchQuery(''); setPage(1); }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>

          <div className="flex items-center gap-2">
            {/* Difficulty filter */}
            <div className="flex gap-1">
              {(['easy', 'medium', 'hard'] as DifficultyLevel[]).map((d) => (
                <Button
                  key={d}
                  variant={selectedDifficulty === d ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => { setSelectedDifficulty(selectedDifficulty === d ? '' : d); setPage(1); }}
                >
                  {d}
                </Button>
              ))}
            </div>

            {/* View toggle */}
            <div className="flex rounded-lg border border-border">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 ${viewMode === 'grid' ? 'bg-primary text-white' : 'text-muted-foreground hover:text-foreground'} rounded-l-lg transition-colors`}
              >
                <Grid3X3 className="h-4 w-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 ${viewMode === 'list' ? 'bg-primary text-white' : 'text-muted-foreground hover:text-foreground'} rounded-r-lg transition-colors`}
              >
                <List className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Loading */}
        {isLoading && (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <Card key={i} className="border-border/50">
                <CardContent className="p-5 space-y-3">
                  <Skeleton className="h-6 w-3/4" />
                  <Skeleton className="h-4 w-1/2" />
                  <Skeleton className="h-4 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!isLoading && words.length === 0 && (
          <EmptyState
            icon={BookOpen}
            title={searchQuery ? 'No words found' : 'No words yet'}
            description={
              searchQuery
                ? 'Try a different search term.'
                : 'Start building your vocabulary by adding your first word!'
            }
            action={
              !searchQuery && (
                <Button onClick={() => setShowAddModal(true)} className="gap-2">
                  <Plus className="h-4 w-4" />
                  Add Your First Word
                </Button>
              )
            }
          />
        )}

        {/* Word Grid / List */}
        {!isLoading && words.length > 0 && (
          <motion.div
            className={
              viewMode === 'grid'
                ? 'grid gap-4 sm:grid-cols-2 lg:grid-cols-3'
                : 'space-y-3'
            }
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {words.map((word) => {
              const dc = difficultyConfig[word.difficulty_level] || difficultyConfig.medium;
              return (
                <motion.div key={word.id} variants={listItemVariants}>
                  <motion.div variants={cardHoverVariants} initial="rest" whileHover="hover" whileTap="tap">
                    <Card
                      className="cursor-pointer border-border/50 overflow-hidden group"
                      onClick={() => setSelectedWord(word)}
                    >
                      <CardContent className={viewMode === 'grid' ? 'p-5' : 'flex items-center gap-4 p-4'}>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <h3 className="font-heading text-lg font-semibold truncate">
                              {word.original_word}
                            </h3>
                            {word.is_mastered && (
                              <Check className="h-4 w-4 text-success shrink-0" />
                            )}
                          </div>
                          {word.translation && (
                            <p className="text-sm text-muted-foreground truncate mt-0.5">
                              {word.translation}
                            </p>
                          )}
                          {word.definition && viewMode === 'grid' && (
                            <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
                              {word.definition}
                            </p>
                          )}
                          {/* Confidence bar */}
                          {word.confidence_score > 0 && viewMode === 'grid' && (
                            <div className="mt-2">
                              <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                                <div
                                  className={cn(
                                    'h-full rounded-full transition-all',
                                    word.confidence_score >= 80 ? 'bg-success' :
                                    word.confidence_score >= 50 ? 'bg-warning' : 'bg-destructive'
                                  )}
                                  style={{ width: `${word.confidence_score}%` }}
                                />
                              </div>
                            </div>
                          )}
                          <div className="flex items-center gap-2 mt-3 flex-wrap">
                            <Badge variant={dc.variant}>{dc.label}</Badge>
                            {word.part_of_speech && (
                              <Badge variant="outline">{word.part_of_speech}</Badge>
                            )}
                            {word.category && (
                              <Badge variant="outline" className="gap-1">
                                <span
                                  className="h-2 w-2 rounded-full"
                                  style={{ backgroundColor: word.category.color }}
                                />
                                {word.category.name}
                              </Badge>
                            )}
                            <EnrichmentStatusBadge status={word.enrichment_status} showLabel={false} />
                          </div>
                        </div>
                        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <ArchiveButton
                            isArchived={false}
                            onArchive={() => archiveWord.mutate(word.id)}
                            onUnarchive={() => {}}
                            size="icon"
                          />
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 text-muted-foreground hover:text-error"
                            onClick={(e) => { e.stopPropagation(); handleDelete(word.id); }}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
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
          <div className="flex items-center justify-center gap-2 pt-4">
            <Button
              variant="outline"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Previous
            </Button>
            <span className="text-sm text-muted-foreground">
              Page {meta.page} of {meta.total_pages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= meta.total_pages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        )}

        {/* Enrich All button */}
        {stats && stats.total > 0 && (
          <div className="flex justify-center pt-2">
            <Button
              variant="outline"
              size="sm"
              className="gap-1.5"
              onClick={() => enrichAll.mutate()}
              disabled={enrichAll.isPending}
            >
              <Sparkles className="h-4 w-4" />
              {enrichAll.isPending ? 'Enriching...' : 'Enrich All Words'}
            </Button>
          </div>
        )}

        </>
        )}

        {/* Word Detail Modal */}
        <AnimatePresence>
          {selectedWord && (
            <WordDetailModal
              word={selectedWord}
              onClose={() => setSelectedWord(null)}
              onDelete={(id) => { handleDelete(id); setSelectedWord(null); }}
            />
          )}
        </AnimatePresence>

        {/* Add Word Modal */}
        <AnimatePresence>
          {showAddModal && <AddWordModal onClose={() => setShowAddModal(false)} />}
        </AnimatePresence>
      </div>
    </PageTransition>
  );
}

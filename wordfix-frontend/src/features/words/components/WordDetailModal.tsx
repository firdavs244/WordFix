import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X, Volume2, Sparkles, BookOpen, MessageSquare, ArrowRight,
  Calendar, BarChart3, Trophy, Tag, Clock,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { EnrichmentStatusBadge } from './EnrichmentStatusBadge';
import { ArchiveButton } from './ArchiveButton';
import { useArchiveWord, useUnarchiveWord, useEnrichWord } from '../hooks/useWords';
import { cn } from '@/lib/utils';
import type { Word, DifficultyLevel } from '@/types';

const difficultyConfig: Record<DifficultyLevel, { color: string; label: string }> = {
  easy: { color: 'bg-success/10 text-success border-success/20', label: 'Easy' },
  medium: { color: 'bg-warning/10 text-warning-foreground border-warning/20', label: 'Medium' },
  hard: { color: 'bg-destructive/10 text-destructive border-destructive/20', label: 'Hard' },
};

function Section({ title, icon: Icon, children }: { title: string; icon: typeof BookOpen; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
        <Icon className="h-3.5 w-3.5" />
        {title}
      </div>
      {children}
    </div>
  );
}

interface WordDetailModalProps {
  word: Word;
  onClose: () => void;
  onDelete?: (id: string) => void;
}

export function WordDetailModal({ word, onClose, onDelete }: WordDetailModalProps) {
  const archiveWord = useArchiveWord();
  const unarchiveWord = useUnarchiveWord();
  const enrichWord = useEnrichWord();

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  const dc = difficultyConfig[word.difficulty_level] || difficultyConfig.medium;
  const accuracy = word.review_count > 0 ? Math.round((word.correct_count / word.review_count) * 100) : 0;

  const playAudio = () => {
    if (word.audio_url) {
      const audio = new Audio(word.audio_url);
      audio.play().catch(() => {});
    }
  };

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <motion.div
          className="relative w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl border border-border/50 bg-card shadow-2xl scrollbar-thin"
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="sticky top-0 z-10 flex items-start justify-between border-b border-border/30 bg-card/95 backdrop-blur-sm p-5 pb-4">
            <div className="flex-1 min-w-0 pr-3">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="font-heading text-2xl font-bold tracking-tight">{word.original_word}</h2>
                {word.audio_url && (
                  <button onClick={playAudio} className="text-muted-foreground hover:text-primary transition-colors">
                    <Volume2 className="h-5 w-5" />
                  </button>
                )}
              </div>
              {word.pronunciation && (
                <p className="mt-0.5 text-sm text-muted-foreground italic">/{word.pronunciation}/</p>
              )}
              <p className="mt-1 text-base text-foreground/80">{word.translation}</p>

              {/* Badges row */}
              <div className="mt-3 flex flex-wrap items-center gap-1.5">
                <Badge className={cn('border', dc.color)}>{dc.label}</Badge>
                {word.part_of_speech && <Badge variant="outline">{word.part_of_speech}</Badge>}
                {word.category && (
                  <Badge variant="outline" className="gap-1">
                    <span className="h-2 w-2 rounded-full" style={{ backgroundColor: word.category.color }} />
                    {word.category.name}
                  </Badge>
                )}
                <EnrichmentStatusBadge status={word.enrichment_status} />
                {word.is_mastered && <Badge variant="success">Mastered</Badge>}
              </div>
            </div>

            <button onClick={onClose} className="rounded-lg p-1.5 hover:bg-muted transition-colors">
              <X className="h-5 w-5 text-muted-foreground" />
            </button>
          </div>

          {/* Content */}
          <div className="space-y-5 p-5">
            {/* Definition */}
            {word.definition && (
              <Section title="Definition" icon={BookOpen}>
                <p className="text-sm leading-relaxed text-foreground/80">{word.definition}</p>
              </Section>
            )}

            {/* Example */}
            {word.example_sentence && (
              <Section title="Example" icon={MessageSquare}>
                <div className="rounded-lg bg-muted/30 px-3 py-2.5">
                  <p className="text-sm italic text-foreground/80">"{word.example_sentence}"</p>
                  {word.example_translation && (
                    <p className="mt-1 text-xs text-muted-foreground">{word.example_translation}</p>
                  )}
                </div>
              </Section>
            )}

            {/* Mnemonic */}
            {word.mnemonic && (
              <Section title="Mnemonic" icon={Sparkles}>
                <p className="text-sm text-foreground/80">{word.mnemonic}</p>
              </Section>
            )}

            {/* Usage notes */}
            {word.usage_notes && (
              <Section title="Usage Notes" icon={Tag}>
                <p className="text-sm text-foreground/80">{word.usage_notes}</p>
              </Section>
            )}

            {/* Related words */}
            {(word.synonyms?.length > 0 || word.antonyms?.length > 0 || word.collocations?.length > 0 || word.word_family?.length > 0) && (
              <Section title="Related Words" icon={ArrowRight}>
                <div className="space-y-2">
                  {word.synonyms?.length > 0 && (
                    <div>
                      <span className="text-[10px] font-medium text-muted-foreground">Synonyms:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {word.synonyms.map((s) => (
                          <span key={s} className="rounded-full bg-success/10 px-2 py-0.5 text-[11px] text-success">{s}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {word.antonyms?.length > 0 && (
                    <div>
                      <span className="text-[10px] font-medium text-muted-foreground">Antonyms:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {word.antonyms.map((a) => (
                          <span key={a} className="rounded-full bg-destructive/10 px-2 py-0.5 text-[11px] text-destructive">{a}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {word.collocations?.length > 0 && (
                    <div>
                      <span className="text-[10px] font-medium text-muted-foreground">Collocations:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {word.collocations.map((c) => (
                          <span key={c} className="rounded-full bg-primary/10 px-2 py-0.5 text-[11px] text-primary">{c}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {word.word_family?.length > 0 && (
                    <div>
                      <span className="text-[10px] font-medium text-muted-foreground">Word Family:</span>
                      <div className="mt-1 flex flex-wrap gap-1">
                        {word.word_family.map((w) => (
                          <span key={w} className="rounded-full bg-accent/10 px-2 py-0.5 text-[11px] text-accent">{w}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Section>
            )}

            {/* Review Stats */}
            <Section title="Review Stats" icon={BarChart3}>
              <div className="grid grid-cols-3 gap-2">
                <div className="rounded-lg bg-muted/30 p-3 text-center">
                  <p className="font-heading text-lg font-bold">{word.review_count}</p>
                  <p className="text-[10px] text-muted-foreground">Reviews</p>
                </div>
                <div className="rounded-lg bg-muted/30 p-3 text-center">
                  <p className="font-heading text-lg font-bold text-success">{accuracy}%</p>
                  <p className="text-[10px] text-muted-foreground">Accuracy</p>
                </div>
                <div className="rounded-lg bg-muted/30 p-3 text-center">
                  <p className="font-heading text-lg font-bold">{word.confidence_score}%</p>
                  <p className="text-[10px] text-muted-foreground">Confidence</p>
                </div>
              </div>

              {/* Confidence bar */}
              <div className="mt-2">
                <div className="flex items-center justify-between text-[10px] text-muted-foreground mb-1">
                  <span>Confidence</span>
                  <span>{word.confidence_score}%</span>
                </div>
                <div className="h-2 rounded-full bg-muted overflow-hidden">
                  <motion.div
                    className={cn(
                      'h-full rounded-full',
                      word.confidence_score >= 80 ? 'bg-success' :
                      word.confidence_score >= 50 ? 'bg-warning' : 'bg-destructive'
                    )}
                    initial={{ width: 0 }}
                    animate={{ width: `${word.confidence_score}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut' }}
                  />
                </div>
              </div>

              {/* SR Info */}
              <div className="mt-2 flex flex-wrap gap-2 text-[10px] text-muted-foreground">
                {word.next_review_at && (
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    Next: {new Date(word.next_review_at).toLocaleDateString()}
                  </span>
                )}
                {word.last_reviewed_at && (
                  <span className="flex items-center gap-1">
                    <Calendar className="h-3 w-3" />
                    Last: {new Date(word.last_reviewed_at).toLocaleDateString()}
                  </span>
                )}
                <span className="flex items-center gap-1">
                  <Trophy className="h-3 w-3" />
                  Interval: {word.interval_days}d
                </span>
              </div>
            </Section>

            {/* Notes */}
            {word.notes && (
              <Section title="Notes" icon={Tag}>
                <p className="text-sm text-foreground/80 whitespace-pre-wrap">{word.notes}</p>
              </Section>
            )}
          </div>

          {/* Footer actions */}
          <div className="sticky bottom-0 flex items-center justify-between border-t border-border/30 bg-card/95 backdrop-blur-sm p-4">
            <div className="flex items-center gap-2">
              <ArchiveButton
                isArchived={word.is_archived}
                onArchive={() => archiveWord.mutate(word.id)}
                onUnarchive={() => unarchiveWord.mutate(word.id)}
                isLoading={archiveWord.isPending || unarchiveWord.isPending}
              />
              {word.enrichment_status !== 'enriched' && word.enrichment_status !== 'processing' && word.enrichment_status !== 'pending' && (
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-1.5"
                  onClick={() => enrichWord.mutate(word.id)}
                  disabled={enrichWord.isPending}
                >
                  <Sparkles className="h-3.5 w-3.5" />
                  Enrich
                </Button>
              )}
            </div>
            {onDelete && (
              <Button
                variant="ghost"
                size="sm"
                className="text-destructive hover:bg-destructive/10"
                onClick={() => { onDelete(word.id); onClose(); }}
              >
                Delete
              </Button>
            )}
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

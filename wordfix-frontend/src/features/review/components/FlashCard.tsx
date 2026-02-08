import { motion } from 'framer-motion';
import { Volume2, Sparkles, BookOpen } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { Word } from '@/types';
import { cn } from '@/lib/utils';

interface FlashCardProps {
  word: Word;
  isFlipped: boolean;
  onFlip: () => void;
}

const difficultyConfig = {
  easy: { label: 'Easy', color: 'bg-success/10 text-success' },
  medium: { label: 'Medium', color: 'bg-warning/10 text-warning-foreground' },
  hard: { label: 'Hard', color: 'bg-error/10 text-error' },
};

export function FlashCard({ word, isFlipped, onFlip }: FlashCardProps) {
  const dc = difficultyConfig[word.difficulty_level] || difficultyConfig.medium;

  return (
    <div
      className="perspective-1000 mx-auto w-full max-w-lg cursor-pointer"
      style={{ perspective: '1000px' }}
      onClick={onFlip}
    >
      <motion.div
        className="relative h-80 w-full"
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, type: 'spring', stiffness: 260, damping: 20 }}
      >
        {/* Front Face */}
        <div
          className={cn(
            'absolute inset-0 rounded-2xl border border-border bg-card p-8 shadow-xl',
            'flex flex-col items-center justify-center backface-hidden',
          )}
          style={{ backfaceVisibility: 'hidden' }}
        >
          <div className="mb-4 flex items-center gap-2">
            <Badge className={dc.color}>{dc.label}</Badge>
            {word.part_of_speech && (
              <Badge variant="outline">{word.part_of_speech}</Badge>
            )}
          </div>

          <h2 className="font-heading text-4xl font-bold text-foreground">
            {word.original_word}
          </h2>

          {word.pronunciation && (
            <p className="mt-2 text-lg text-muted-foreground">
              /{word.pronunciation}/
            </p>
          )}

          <div className="mt-6 flex items-center gap-2 text-sm text-muted-foreground">
            <BookOpen className="h-4 w-4" />
            <span>Tap to reveal answer</span>
          </div>

          {word.audio_url && (
            <Button
              variant="ghost"
              size="icon"
              className="mt-4"
              onClick={(e) => {
                e.stopPropagation();
                const audio = new Audio(word.audio_url);
                audio.play();
              }}
            >
              <Volume2 className="h-5 w-5" />
            </Button>
          )}
        </div>

        {/* Back Face */}
        <div
          className={cn(
            'absolute inset-0 rounded-2xl border border-border bg-card p-8 shadow-xl',
            'flex flex-col items-center justify-center overflow-y-auto backface-hidden',
          )}
          style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
        >
          {word.translation && (
            <h3 className="font-heading text-2xl font-bold text-primary">
              {word.translation}
            </h3>
          )}

          {word.definition && (
            <p className="mt-3 text-center text-sm text-muted-foreground">
              {word.definition}
            </p>
          )}

          {word.example_sentence && (
            <div className="mt-4 rounded-lg bg-muted/50 px-4 py-2">
              <p className="text-sm italic text-foreground">
                "{word.example_sentence}"
              </p>
              {word.example_translation && (
                <p className="mt-1 text-xs text-muted-foreground">
                  {word.example_translation}
                </p>
              )}
            </div>
          )}

          {word.mnemonic && (
            <div className="mt-3 flex items-center gap-2 text-sm text-primary">
              <Sparkles className="h-4 w-4" />
              <span>{word.mnemonic}</span>
            </div>
          )}

          {(word.synonyms?.length > 0 || word.antonyms?.length > 0) && (
            <div className="mt-3 flex flex-wrap gap-1">
              {word.synonyms?.slice(0, 3).map((s) => (
                <Badge key={s} variant="outline" className="text-xs">
                  ≈ {s}
                </Badge>
              ))}
              {word.antonyms?.slice(0, 2).map((a) => (
                <Badge key={a} variant="outline" className="text-xs text-error">
                  ≠ {a}
                </Badge>
              ))}
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

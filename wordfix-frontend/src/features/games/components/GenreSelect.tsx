import { motion } from 'framer-motion';
import { Check, ChevronRight, Loader2, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PageTransition } from '@/components/animations/PageTransition';
import { BookOpen, GENRES } from './storyBuilderHelpers';

interface GenreSelectProps {
  selectedGenre: string | null;
  onSelectGenre: (genre: string) => void;
  onStart: () => void;
  isPending: boolean;
}

export function GenreSelect({
  selectedGenre,
  onSelectGenre,
  onStart,
  isPending,
}: GenreSelectProps) {
  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-8 py-8">
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', bounce: 0.4 }}
            className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-purple-500/10"
          >
            <BookOpen className="h-8 w-8 text-purple-500" />
          </motion.div>
          <h1 className="text-2xl font-bold">Story Builder</h1>
          <p className="mt-2 text-muted-foreground">Choose a genre for your story</p>
        </div>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          {GENRES.map((genre, i) => (
            <motion.button
              key={genre.key}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              onClick={() => onSelectGenre(genre.key)}
              className={`relative flex flex-col items-center gap-2 rounded-xl border-2 p-4 transition-all hover:scale-105 hover:shadow-md ${
                selectedGenre === genre.key
                  ? 'border-primary bg-primary/10 shadow-md'
                  : 'border-border hover:border-primary/50'
              }`}
            >
              {selectedGenre === genre.key && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute -right-1.5 -top-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-primary-foreground"
                >
                  <Check className="h-3 w-3" />
                </motion.div>
              )}
              <span className="text-2xl">{genre.emoji}</span>
              <span className="text-sm font-medium">{genre.label}</span>
            </motion.button>
          ))}
        </div>

        <div className="flex justify-center">
          <Button
            size="lg"
            disabled={!selectedGenre || isPending}
            onClick={onStart}
            className="gap-2"
          >
            {isPending ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
            Start Story
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </PageTransition>
  );
}

import { useState } from 'react';
import { Loader2, Type, Languages } from 'lucide-react';
import { AuthInput } from '@/features/auth/components/AuthInput';
import AddWordDifficultySelector from './AddWordDifficultySelector';
import { useCreateWord } from '../hooks/useWords';
import type { DifficultyLevel, WordCreateData } from '@/types';

interface Props {
  onSuccess: () => void;
}

export default function AddWordForm({ onSuccess }: Props) {
  const createWord = useCreateWord();
  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState('');
  const [definition, setDefinition] = useState('');
  const [example, setExample] = useState('');
  const [difficulty, setDifficulty] = useState<DifficultyLevel>('medium');
  const [notes, setNotes] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!word.trim()) return;
    const data: WordCreateData = {
      original_word: word.trim(),
      translation: translation.trim() || undefined,
      definition: definition.trim() || undefined,
      example_sentence: example.trim() || undefined,
      difficulty_level: difficulty,
      notes: notes.trim() || undefined,
    };
    try {
      await createWord.mutateAsync(data);
      onSuccess();
    } catch { /* handled by mutation */ }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="max-h-[65vh] space-y-4 overflow-y-auto px-6 py-5 scrollbar-thin">
        <AuthInput icon={Type} label="Word" placeholder="Enter the word" value={word} onChange={setWord} />
        <AuthInput icon={Languages} label="Translation" placeholder="Enter translation" value={translation} onChange={setTranslation} />
        <div>
          <label className="mb-1.5 block text-sm font-medium">Definition</label>
          <textarea
            placeholder="Enter definition"
            value={definition}
            onChange={(e) => setDefinition(e.target.value)}
            className="h-20 w-full resize-none rounded-xl border border-border/50 bg-background p-3 text-sm placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
          />
        </div>
        <div>
          <label className="mb-1.5 block text-sm font-medium">Example Sentence</label>
          <textarea
            placeholder="Enter example sentence"
            value={example}
            onChange={(e) => setExample(e.target.value)}
            className="h-20 w-full resize-none rounded-xl border border-border/50 bg-background p-3 text-sm placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
          />
        </div>
        <AddWordDifficultySelector value={difficulty} onChange={setDifficulty} />
        <div>
          <label className="mb-1.5 block text-sm font-medium">Notes</label>
          <textarea
            placeholder="Personal notes..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="h-16 w-full resize-none rounded-xl border border-border/50 bg-background p-3 text-sm placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
          />
        </div>
      </div>
      <div className="flex gap-3 border-t border-border/30 bg-card px-6 py-4">
        <button type="button" onClick={onSuccess} className="flex-1 rounded-xl border border-border/50 py-2.5 text-sm font-medium transition-colors hover:bg-muted">
          Cancel
        </button>
        <button type="submit" disabled={!word.trim() || createWord.isPending} className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 py-2.5 text-sm font-medium text-white transition-all disabled:opacity-50">
          {createWord.isPending ? <><Loader2 className="h-4 w-4 animate-spin" /> Adding...</> : 'Add Word'}
        </button>
      </div>
    </form>
  );
}

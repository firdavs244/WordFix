import { useState } from 'react';
import { motion } from 'framer-motion';
import { Plus, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { useCreateWord, useCategories } from '../hooks/useWords';
import type { DifficultyLevel, WordCreateData } from '@/types';
import { toast } from 'sonner';

interface AddWordModalProps {
  onClose: () => void;
}

export function AddWordModal({ onClose }: AddWordModalProps) {
  const createWord = useCreateWord();
  const { data: categoriesData } = useCategories();
  const categories = categoriesData?.data ?? [];

  const [word, setWord] = useState('');
  const [translation, setTranslation] = useState('');
  const [definition, setDefinition] = useState('');
  const [exampleSentence, setExampleSentence] = useState('');
  const [difficulty, setDifficulty] = useState<DifficultyLevel>('medium');
  const [notes, setNotes] = useState('');
  const [categoryId, setCategoryId] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!word.trim()) {
      toast.error('Word is required.');
      return;
    }

    const data: WordCreateData = {
      original_word: word.trim(),
      translation: translation.trim() || undefined,
      definition: definition.trim() || undefined,
      example_sentence: exampleSentence.trim() || undefined,
      difficulty_level: difficulty,
      notes: notes.trim() || undefined,
      category_id: categoryId || undefined,
    };

    try {
      await createWord.mutateAsync(data);
      onClose();
    } catch {
      // Error handled by mutation
    }
  };

  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="w-full max-w-lg"
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        <Card className="border-border/50 shadow-2xl">
          <div className="flex items-center justify-between p-6 pb-2">
            <h2 className="font-heading text-xl font-semibold">Add New Word</h2>
            <button onClick={onClose} className="text-muted-foreground hover:text-foreground">
              <X className="h-5 w-5" />
            </button>
          </div>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4 max-h-[60vh] overflow-y-auto">
              <div className="space-y-2">
                <label className="text-sm font-medium">Word *</label>
                <Input
                  placeholder="e.g., ubiquitous"
                  value={word}
                  onChange={(e) => setWord(e.target.value)}
                  autoFocus
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Translation</label>
                <Input
                  placeholder="e.g., hamma joyda mavjud"
                  value={translation}
                  onChange={(e) => setTranslation(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Definition</label>
                <Input
                  placeholder="e.g., Present, appearing, or found everywhere"
                  value={definition}
                  onChange={(e) => setDefinition(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Example Sentence</label>
                <Input
                  placeholder="e.g., Smartphones have become ubiquitous."
                  value={exampleSentence}
                  onChange={(e) => setExampleSentence(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Difficulty</label>
                <div className="flex gap-2">
                  {(['easy', 'medium', 'hard'] as DifficultyLevel[]).map((d) => (
                    <Button
                      key={d}
                      type="button"
                      variant={difficulty === d ? 'default' : 'outline'}
                      size="sm"
                      onClick={() => setDifficulty(d)}
                    >
                      {d}
                    </Button>
                  ))}
                </div>
              </div>
              {categories.length > 0 && (
                <div className="space-y-2">
                  <label className="text-sm font-medium">Category</label>
                  <select
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                    value={categoryId}
                    onChange={(e) => setCategoryId(e.target.value)}
                  >
                    <option value="">None</option>
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
              )}
              <div className="space-y-2">
                <label className="text-sm font-medium">Notes</label>
                <Input
                  placeholder="Any personal notes..."
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </div>
            </CardContent>
            <div className="flex justify-end gap-2 p-6 pt-2">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={createWord.isPending} className="gap-2">
                {createWord.isPending ? (
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                ) : (
                  <Plus className="h-4 w-4" />
                )}
                Add Word
              </Button>
            </div>
          </form>
        </Card>
      </motion.div>
    </motion.div>
  );
}

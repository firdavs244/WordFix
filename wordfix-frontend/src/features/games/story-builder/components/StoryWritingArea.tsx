import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';

interface Props {
  targetWords: string[];
  onSubmit: (text: string) => void;
  isSubmitting: boolean;
}

export default function StoryWritingArea({ targetWords, onSubmit, isSubmitting }: Props) {
  const [text, setText] = useState('');

  const handleSubmit = () => {
    if (text.trim()) onSubmit(text.trim());
  };

  return (
    <div className="mt-4">
      <div className="mb-2 flex flex-wrap gap-1.5">
        <span className="text-xs text-muted-foreground">Use these words:</span>
        {targetWords.map((w) => (
          <span key={w} className="rounded bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">{w}</span>
        ))}
      </div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Continue the story using the target words..."
        rows={4}
        className="w-full resize-none rounded-xl border border-border/50 bg-background p-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
        data-testid="story-textarea"
      />
      <button
        type="button"
        onClick={handleSubmit}
        disabled={!text.trim() || isSubmitting}
        className="mt-2 flex h-10 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-medium text-white disabled:opacity-50"
      >
        {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        Submit Continuation
      </button>
    </div>
  );
}

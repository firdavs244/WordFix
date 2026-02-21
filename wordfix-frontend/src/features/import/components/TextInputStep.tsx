import { cn } from '@/lib/utils';

interface TextInputStepProps {
  text: string;
  onChange: (text: string) => void;
}

export default function TextInputStep({ text, onChange }: TextInputStepProps) {
  const count = text.length;

  return (
    <div className="rounded-2xl border border-border/50 p-6 shadow-card">
      <textarea
        value={text}
        onChange={(e) => onChange(e.target.value.slice(0, 5000))}
        placeholder="Paste your English text here... Articles, stories, or any content with words you want to learn."
        className="h-48 w-full resize-none rounded-xl border border-border/50 bg-background px-4 py-3 text-sm leading-relaxed transition-all placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
      />
      <div className="mt-4 flex items-center justify-between">
        <span
          className={cn(
            'text-xs',
            count >= 5000 ? 'text-destructive' : count >= 4500 ? 'text-warning' : 'text-muted-foreground',
          )}
        >
          {count}/5000
        </span>
      </div>
    </div>
  );
}

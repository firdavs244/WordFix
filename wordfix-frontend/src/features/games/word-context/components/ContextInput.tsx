import { useState, useRef, useEffect } from 'react';
import { SendHorizontal } from 'lucide-react';

interface Props {
  onSubmit: (answer: string) => void;
  disabled: boolean;
}

export default function ContextInput({ onSubmit, disabled }: Props) {
  const [value, setValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { inputRef.current?.focus(); }, []);

  const handleSubmit = () => {
    if (value.trim() && !disabled) {
      onSubmit(value.trim());
      setValue('');
    }
  };

  return (
    <div className="mt-4 flex gap-2">
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
        placeholder="Type the missing word..."
        disabled={disabled}
        className="h-11 flex-1 rounded-xl border border-border/50 bg-background px-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
        aria-label="Context answer input"
      />
      <button
        type="button"
        onClick={handleSubmit}
        disabled={!value.trim() || disabled}
        className="flex h-11 w-11 items-center justify-center rounded-xl bg-primary text-white disabled:opacity-50"
        aria-label="Submit"
      >
        <SendHorizontal className="h-[18px] w-[18px]" />
      </button>
    </div>
  );
}

import { useState } from 'react';
import { Search } from 'lucide-react';
import { cn } from '@/lib/utils';

export function SearchBar() {
  const [focused, setFocused] = useState(false);

  return (
    <div className={cn('relative transition-all duration-300', focused ? 'w-96' : 'w-64')}>
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
      <input
        type="text"
        placeholder="Search words..."
        className={cn(
          'h-9 w-full rounded-lg bg-muted/50 pl-9 pr-12 text-sm outline-none transition-all placeholder:text-muted-foreground/60',
          focused && 'bg-background ring-1 ring-ring/20 shadow-sm',
        )}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
      />
      {!focused && (
        <kbd className="absolute right-3 top-1/2 -translate-y-1/2 rounded bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground/50">
          ⌘K
        </kbd>
      )}
    </div>
  );
}

import { X } from 'lucide-react';

interface Props {
  current: number;
  total: number;
  onQuit: () => void;
}

export default function TestSessionTopBar({ current, total, onQuit }: Props) {
  return (
    <div className="fixed left-0 top-0 z-30 flex h-14 w-full items-center justify-between border-b border-border/20 bg-background/80 px-4 backdrop-blur-xl lg:px-6">
      <button
        onClick={onQuit}
        className="flex h-9 items-center gap-1.5 rounded-lg px-3 text-muted-foreground transition-colors hover:text-destructive"
      >
        <X className="h-[18px] w-[18px]" />
        <span className="hidden text-sm sm:inline">Quit</span>
      </button>
      <p className="text-sm font-medium">
        Q <span className="font-semibold text-primary">{current + 1}</span>/{total}
      </p>
      <div className="w-16" />
    </div>
  );
}

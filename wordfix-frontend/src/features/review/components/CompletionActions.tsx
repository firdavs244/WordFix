import { Home, Repeat } from 'lucide-react';

interface Props {
  onDashboard: () => void;
  onReviewAgain: () => void;
}

export default function CompletionActions({ onDashboard, onReviewAgain }: Props) {
  return (
    <div className="mt-6 flex gap-3">
      <button onClick={onDashboard} className="flex flex-1 items-center justify-center gap-2 rounded-xl border border-border/50 py-2.5 text-sm font-medium transition-colors hover:bg-muted">
        <Home className="h-4 w-4" /> Dashboard
      </button>
      <button onClick={onReviewAgain} className="flex flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 py-2.5 text-sm font-medium text-white transition-all hover:shadow-glow-primary">
        <Repeat className="h-4 w-4" /> Review Again
      </button>
    </div>
  );
}

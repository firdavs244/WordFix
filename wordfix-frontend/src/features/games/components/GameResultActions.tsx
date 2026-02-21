import { Link } from 'react-router-dom';
import { RotateCcw, LayoutDashboard } from 'lucide-react';

interface Props {
  playAgainHref?: string;
  gameRoute?: string;
  dashboardRoute?: string;
}

export default function GameResultActions({ playAgainHref, gameRoute, dashboardRoute }: Props) {
  const playHref = gameRoute ?? playAgainHref ?? '/games';
  const dashHref = dashboardRoute ?? '/dashboard';
  return (
    <div className="flex gap-3" data-testid="result-actions">
      <Link
        to={playHref}
        className="flex h-10 flex-1 items-center justify-center gap-2 rounded-xl bg-primary text-sm font-medium text-white"
      >
        <RotateCcw className="h-4 w-4" /> Play Again
      </Link>
      <Link
        to={dashHref}
        className="flex h-10 flex-1 items-center justify-center gap-2 rounded-xl border border-border/50 text-sm font-medium"
      >
        <LayoutDashboard className="h-4 w-4" /> Dashboard
      </Link>
    </div>
  );
}

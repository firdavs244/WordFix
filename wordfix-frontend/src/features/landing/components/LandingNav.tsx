import { Link } from 'react-router-dom';
import { Logo } from '@/components/shared';

export function LandingNav() {
  return (
    <header className="fixed top-0 z-50 w-full border-b border-border/20 bg-background/60 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <Logo size="md" />
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-muted-foreground transition hover:text-foreground">
            Sign In
          </Link>
          <Link
            to="/register"
            className="rounded-xl bg-primary px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:shadow-glow-primary"
          >
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

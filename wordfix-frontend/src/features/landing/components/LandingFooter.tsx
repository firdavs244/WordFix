import { Logo } from '@/components/shared';
import { APP_VERSION } from '@/lib/constants';

export function LandingFooter() {
  return (
    <footer className="border-t border-border/30 px-6 py-12">
      <div className="mx-auto flex max-w-6xl items-center justify-between">
        <div className="flex items-center gap-3">
          <Logo size="sm" />
          <span className="text-xs text-muted-foreground">&copy; 2025 WordFix. All rights reserved.</span>
        </div>
        <span className="text-[10px] text-muted-foreground/30">v{APP_VERSION}</span>
      </div>
    </footer>
  );
}

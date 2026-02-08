import { BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LogoProps {
  collapsed?: boolean;
  className?: string;
}

export function Logo({ collapsed = false, className }: LogoProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary shadow-lg shadow-primary/25">
        <BookOpen className="h-5 w-5 text-white" />
      </div>
      {!collapsed && (
        <div className="flex flex-col">
          <span className="font-heading text-xl font-bold text-foreground">
            Word<span className="text-primary">Fix</span>
          </span>
        </div>
      )}
    </div>
  );
}

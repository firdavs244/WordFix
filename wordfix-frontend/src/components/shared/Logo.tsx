import { BookOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  className?: string;
}

const sizes = { sm: 'h-7 w-7', md: 'h-9 w-9', lg: 'h-11 w-11' };
const iconSizes = { sm: 'h-4 w-4', md: 'h-5 w-5', lg: 'h-6 w-6' };
const textSizes = { sm: 'text-lg', md: 'text-xl', lg: 'text-2xl' };

export default function Logo({ size = 'md', showText = true, className }: LogoProps) {
  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className={cn('flex items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary/80 shadow-glow-primary', sizes[size])}>
        <BookOpen className={cn('text-white', iconSizes[size])} />
      </div>
      {showText && (
        <span className={cn('font-heading font-bold', textSizes[size])}>
          Word<span className="text-gradient">Fix</span>
        </span>
      )}
    </div>
  );
}

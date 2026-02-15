import { type ReactNode, createElement } from 'react';
import { cn } from '@/lib/utils';

interface GradientTextProps {
  children: ReactNode;
  className?: string;
  as?: 'span' | 'h1' | 'h2' | 'h3' | 'p';
}

export default function GradientText({ children, className, as = 'span' }: GradientTextProps) {
  return createElement(as, { className: cn('text-gradient', className) }, children);
}

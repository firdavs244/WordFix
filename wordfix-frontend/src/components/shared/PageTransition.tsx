import { motion } from 'framer-motion';
import type { ReactNode } from 'react';
import { pageTransition } from '@/lib/motion';
import { cn } from '@/lib/utils';

interface PageTransitionProps {
  children: ReactNode;
  className?: string;
}

export default function PageTransition({ children, className }: PageTransitionProps) {
  return (
    <motion.div variants={pageTransition} initial="initial" animate="animate" exit="exit" className={cn(className)}>
      {children}
    </motion.div>
  );
}

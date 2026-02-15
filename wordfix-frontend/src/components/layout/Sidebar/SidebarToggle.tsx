import { motion, AnimatePresence } from 'framer-motion';
import { ChevronsLeft } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarToggleProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function SidebarToggle({ collapsed, onToggle }: SidebarToggleProps) {
  return (
    <div className="px-3 py-2">
      <button
        onClick={onToggle}
        className={cn(
          'flex h-9 w-full items-center rounded-lg text-muted-foreground transition-colors hover:bg-muted/50 hover:text-foreground',
          collapsed ? 'justify-center' : 'gap-3 px-3',
        )}
        aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        <motion.div animate={{ rotate: collapsed ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronsLeft size={18} strokeWidth={1.75} />
        </motion.div>
        <AnimatePresence>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0, width: 0 }}
              animate={{ opacity: 1, width: 'auto' }}
              exit={{ opacity: 0, width: 0 }}
              className="overflow-hidden whitespace-nowrap text-sm"
            >
              Collapse
            </motion.span>
          )}
        </AnimatePresence>
      </button>
    </div>
  );
}

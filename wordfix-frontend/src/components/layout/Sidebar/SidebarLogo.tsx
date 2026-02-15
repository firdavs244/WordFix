import { AnimatePresence, motion } from 'framer-motion';
import { Logo } from '@/components/shared';

interface SidebarLogoProps {
  collapsed: boolean;
}

export function SidebarLogo({ collapsed }: SidebarLogoProps) {
  return (
    <div className="flex h-14 items-center px-4">
      <Logo size="sm" showText={false} />
      <AnimatePresence>
        {!collapsed && (
          <motion.span
            initial={{ opacity: 0, width: 0 }}
            animate={{ opacity: 1, width: 'auto' }}
            exit={{ opacity: 0, width: 0 }}
            transition={{ duration: 0.15 }}
            className="ml-2 overflow-hidden whitespace-nowrap font-heading font-bold text-lg"
          >
            Word<span className="text-gradient">Fix</span>
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  );
}

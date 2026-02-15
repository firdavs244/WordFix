import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import type { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarNavItemProps {
  to: string;
  icon: LucideIcon;
  label: string;
  collapsed: boolean;
}

export function SidebarNavItem({ to, icon: Icon, label, collapsed }: SidebarNavItemProps) {
  return (
    <NavLink
      to={to}
      title={collapsed ? label : undefined}
      className={({ isActive }) =>
        cn(
          'relative flex h-10 items-center gap-3 rounded-lg px-3 transition-colors duration-150',
          isActive
            ? 'bg-primary/10 font-semibold text-primary dark:bg-primary/15'
            : 'text-muted-foreground hover:bg-muted/50 hover:text-foreground',
        )
      }
    >
      {({ isActive }) => (
        <>
          {isActive && (
            <motion.div
              layoutId="sidebar-active-indicator"
              className="absolute left-0 h-5 w-[3px] rounded-full bg-primary"
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            />
          )}
          <Icon size={20} strokeWidth={1.75} className="shrink-0" />
          <AnimatePresence>
            {!collapsed && (
              <motion.span
                initial={{ opacity: 0, x: -8 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -8 }}
                transition={{ duration: 0.15 }}
                className="overflow-hidden whitespace-nowrap text-sm"
              >
                {label}
              </motion.span>
            )}
          </AnimatePresence>
        </>
      )}
    </NavLink>
  );
}

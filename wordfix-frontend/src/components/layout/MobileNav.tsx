import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Home, BookOpen, ClipboardCheck, Gamepad2, User } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MobileNavItem {
  to: string;
  icon: LucideIcon;
  label: string;
}

const items: MobileNavItem[] = [
  { to: '/', icon: Home, label: 'Home' },
  { to: '/words', icon: BookOpen, label: 'Words' },
  { to: '/tests', icon: ClipboardCheck, label: 'Tests' },
  { to: '/games', icon: Gamepad2, label: 'Games' },
  { to: '/profile', icon: User, label: 'Profile' },
];

export function MobileNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-40 grid h-16 grid-cols-5 items-center border-t border-border/40 glass shadow-lg pb-[env(safe-area-inset-bottom)] lg:hidden">
      {items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            cn(
              'flex flex-col items-center gap-0.5 text-[10px] font-medium transition-colors',
              isActive ? 'text-primary' : 'text-muted-foreground hover:text-foreground',
            )
          }
        >
          {({ isActive }) => (
            <>
              <item.icon size={20} strokeWidth={isActive ? 2.25 : 1.75} />
              <span>{item.label}</span>
              {isActive && (
                <motion.div
                  layoutId="mobile-nav-indicator"
                  className="h-1 w-1 rounded-full bg-primary"
                  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                />
              )}
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}

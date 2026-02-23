import { useState, useCallback } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  BookOpen,
  Gamepad2,
  User,
  MoreHorizontal,
  X,
  ClipboardCheck,
  RotateCcw,
  Import,
  MessageSquare,
  BarChart3,
  ArrowLeftRight,
  Award,
  Bell,
  GraduationCap,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MobileNavItem {
  to: string;
  icon: LucideIcon;
  label: string;
}

const mainItems: MobileNavItem[] = [
  { to: '/', icon: Home, label: 'Home' },
  { to: '/words', icon: BookOpen, label: 'Words' },
  { to: '/games', icon: Gamepad2, label: 'Games' },
  { to: '/profile', icon: User, label: 'Profile' },
];

const moreItems: MobileNavItem[] = [
  { to: '/tests', icon: ClipboardCheck, label: 'Tests' },
  { to: '/review', icon: RotateCcw, label: 'Review' },
  { to: '/import', icon: Import, label: 'Import' },
  { to: '/chat', icon: MessageSquare, label: 'AI Chat' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/confusing-pairs', icon: ArrowLeftRight, label: 'Confusing Pairs' },
  { to: '/badges', icon: Award, label: 'Badges' },
  { to: '/notifications', icon: Bell, label: 'Notifications' },
  { to: '/learning-profile', icon: GraduationCap, label: 'Learning Profile' },
];

export function MobileNav() {
  const [sheetOpen, setSheetOpen] = useState(false);
  const navigate = useNavigate();

  const handleMoreItemClick = useCallback(
    (to: string) => {
      setSheetOpen(false);
      navigate(to);
    },
    [navigate],
  );

  return (
    <>
      {/* Bottom tab bar */}
      <nav className="fixed bottom-0 left-0 right-0 z-40 grid h-16 grid-cols-5 items-center border-t border-border/40 glass shadow-lg pb-[env(safe-area-inset-bottom)] lg:hidden">
        {mainItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
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

        {/* More button */}
        <button
          onClick={() => setSheetOpen(true)}
          className={cn(
            'flex flex-col items-center gap-0.5 text-[10px] font-medium transition-colors',
            sheetOpen ? 'text-primary' : 'text-muted-foreground hover:text-foreground',
          )}
        >
          <MoreHorizontal size={20} strokeWidth={1.75} />
          <span>More</span>
        </button>
      </nav>

      {/* More sheet overlay */}
      <AnimatePresence>
        {sheetOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm lg:hidden"
              onClick={() => setSheetOpen(false)}
            />

            {/* Sheet */}
            <motion.div
              initial={{ y: '100%' }}
              animate={{ y: 0 }}
              exit={{ y: '100%' }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
              className="fixed bottom-0 left-0 right-0 z-50 rounded-t-2xl border-t border-border/40 bg-background shadow-2xl lg:hidden"
            >
              {/* Handle + close */}
              <div className="flex items-center justify-between px-5 pt-3 pb-2">
                <div className="h-1 w-10 rounded-full bg-muted-foreground/20" />
                <button onClick={() => setSheetOpen(false)} className="rounded-lg p-1 hover:bg-muted/40">
                  <X size={18} className="text-muted-foreground" />
                </button>
              </div>

              {/* Grid of items */}
              <div className="grid grid-cols-3 gap-1 px-4 pb-6">
                {moreItems.map((item) => (
                  <button
                    key={item.to}
                    onClick={() => handleMoreItemClick(item.to)}
                    className="flex flex-col items-center gap-1.5 rounded-xl p-3 text-[11px] font-medium text-muted-foreground transition-colors hover:bg-muted/40 hover:text-foreground active:bg-muted/60"
                  >
                    <item.icon size={22} strokeWidth={1.75} />
                    <span className="leading-tight">{item.label}</span>
                  </button>
                ))}
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

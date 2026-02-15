import { Fragment } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Home, BookOpen, Upload, Brain, MessageCircle,
  ClipboardCheck, Shuffle, Gamepad2, BarChart3,
  GraduationCap, Award, User,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { SidebarNavItem } from './SidebarNavItem';

interface NavGroup {
  label?: string;
  items: { to: string; icon: LucideIcon; label: string }[];
}

const groups: NavGroup[] = [
  {
    items: [
      { to: '/', icon: Home, label: 'Home' },
      { to: '/words', icon: BookOpen, label: 'Words' },
      { to: '/import', icon: Upload, label: 'Import' },
    ],
  },
  {
    label: 'PRACTICE',
    items: [
      { to: '/review', icon: Brain, label: 'Review' },
      { to: '/chat', icon: MessageCircle, label: 'Chat' },
      { to: '/tests', icon: ClipboardCheck, label: 'Tests' },
    ],
  },
  {
    label: 'GAMES & CHALLENGES',
    items: [
      { to: '/confusing-pairs', icon: Shuffle, label: 'Confusing Pairs' },
      { to: '/games', icon: Gamepad2, label: 'Games' },
    ],
  },
  {
    label: 'PROGRESS',
    items: [
      { to: '/analytics', icon: BarChart3, label: 'Analytics' },
      { to: '/learning-profile', icon: GraduationCap, label: 'Learning Profile' },
      { to: '/badges', icon: Award, label: 'Badges' },
      { to: '/profile', icon: User, label: 'Profile' },
    ],
  },
];

interface SidebarNavProps {
  collapsed: boolean;
}

export function SidebarNav({ collapsed }: SidebarNavProps) {
  return (
    <nav className="flex-1 overflow-y-auto scrollbar-thin px-3">
      {groups.map((group, gi) => (
        <Fragment key={gi}>
          <div className="mb-6">
            {group.label && (
              <AnimatePresence>
                {!collapsed && (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="mb-2 px-3 text-[10px] font-semibold uppercase tracking-[0.08em] text-muted-foreground/60"
                  >
                    {group.label}
                  </motion.p>
                )}
              </AnimatePresence>
            )}
            <div className="flex flex-col gap-0.5">
              {group.items.map((item) => (
                <SidebarNavItem key={item.to} {...item} collapsed={collapsed} />
              ))}
            </div>
          </div>
        </Fragment>
      ))}
    </nav>
  );
}

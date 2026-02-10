import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Home,
  BookOpen,
  Gamepad2,
  BarChart3,
  User,
  ChevronLeft,
  ChevronRight,
  Brain,
  ClipboardCheck,
  Award,
  Upload,
  MessageCircle,
  Shuffle,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAppStore } from '@/stores/useAppStore';
import { Logo } from '@/components/common/Logo';
import { Separator } from '@/components/ui/separator';

const navItems = [
  { label: 'Home', path: '/', icon: Home },
  { label: 'Words', path: '/words', icon: BookOpen },
  { label: 'Import', path: '/import', icon: Upload },
  { label: 'Review', path: '/review', icon: Brain },
  { label: 'Chat', path: '/chat', icon: MessageCircle },
  { label: 'Tests', path: '/tests', icon: ClipboardCheck },
  { label: 'Confusing Pairs', path: '/confusing-pairs', icon: Shuffle },
  { label: 'Games', path: '/games', icon: Gamepad2 },
  { label: 'Analytics', path: '/analytics', icon: BarChart3 },
  { label: 'Badges', path: '/badges', icon: Award },
  { label: 'Profile', path: '/profile', icon: User },
];

export function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useAppStore();

  return (
    <motion.aside
      className="relative flex h-full flex-col border-r border-sidebar-border bg-sidebar"
      animate={{ width: sidebarCollapsed ? 72 : 240 }}
      transition={{ duration: 0.2, ease: 'easeInOut' }}
    >
      {/* Logo */}
      <div className="flex h-16 items-center px-4">
        <Logo collapsed={sidebarCollapsed} />
      </div>

      <Separator />

      {/* Navigation */}
      <nav className="flex flex-1 flex-col gap-1 p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                'group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-sidebar-accent text-primary'
                  : 'text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground',
              )
            }
          >
            <item.icon className="h-5 w-5 shrink-0" />
            <AnimatePresence mode="wait">
              {!sidebarCollapsed && (
                <motion.span
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: 'auto' }}
                  exit={{ opacity: 0, width: 0 }}
                  transition={{ duration: 0.15 }}
                  className="overflow-hidden whitespace-nowrap"
                >
                  {item.label}
                </motion.span>
              )}
            </AnimatePresence>
          </NavLink>
        ))}
      </nav>

      {/* Collapse toggle */}
      <div className="border-t border-sidebar-border p-3">
        <button
          onClick={toggleSidebar}
          className="flex w-full items-center justify-center rounded-lg p-2 text-sidebar-foreground/50 transition-colors hover:bg-sidebar-accent hover:text-sidebar-foreground"
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {sidebarCollapsed ? (
            <ChevronRight className="h-5 w-5" />
          ) : (
            <ChevronLeft className="h-5 w-5" />
          )}
        </button>
      </div>
    </motion.aside>
  );
}

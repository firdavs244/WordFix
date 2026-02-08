import { NavLink } from 'react-router-dom';
import { Home, BookOpen, ClipboardCheck, Gamepad2, User } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { label: 'Home', path: '/', icon: Home },
  { label: 'Words', path: '/words', icon: BookOpen },
  { label: 'Tests', path: '/tests', icon: ClipboardCheck },
  { label: 'Games', path: '/games', icon: Gamepad2 },
  { label: 'Profile', path: '/profile', icon: User },
];

/**
 * Mobile bottom navigation bar.
 *
 * Visible only on screens smaller than lg breakpoint.
 * Fixed to the bottom of the viewport.
 */
export function MobileNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-around border-t border-border bg-card/95 backdrop-blur-lg lg:hidden">
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            cn(
              'flex flex-col items-center gap-0.5 px-3 py-1 text-[11px] font-medium transition-colors',
              isActive
                ? 'text-primary'
                : 'text-muted-foreground hover:text-foreground',
            )
          }
        >
          <item.icon className="h-5 w-5" />
          <span>{item.label}</span>
        </NavLink>
      ))}
    </nav>
  );
}

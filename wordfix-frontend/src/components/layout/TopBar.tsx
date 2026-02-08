import { Search, Sun, Moon, Monitor, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Logo } from '@/components/common/Logo';
import { useTheme } from '@/hooks/useTheme';
import { useMediaQuery } from '@/hooks/useMediaQuery';
import { Separator } from '@/components/ui/separator';
import { useAuthStore } from '@/stores/useAuthStore';
import { StreakWidget } from '@/features/review/components/StreakWidget';
import { LevelProgress } from '@/features/progress/components/LevelProgress';
import { NotificationBell } from '@/features/progress/components/NotificationBell';

export function TopBar() {
  const { theme, setTheme } = useTheme();
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  const cycleTheme = () => {
    if (theme === 'light') setTheme('dark');
    else if (theme === 'dark') setTheme('system');
    else setTheme('light');
  };

  const ThemeIcon = theme === 'light' ? Sun : theme === 'dark' ? Moon : Monitor;

  return (
    <header className="flex h-16 shrink-0 items-center border-b border-border bg-card/80 px-4 backdrop-blur-lg lg:px-6">
      {/* Logo (mobile only) */}
      {!isDesktop && <Logo className="mr-4" />}

      {/* Search */}
      <div className="relative flex-1 lg:max-w-md">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search words..."
          className="pl-9 bg-background"
        />
      </div>

      <div className="flex items-center gap-2 ml-4">
        {/* Level & XP */}
        <LevelProgress compact />

        <Separator orientation="vertical" className="h-6 mx-1" />

        {/* Streak */}
        <StreakWidget compact />

        <Separator orientation="vertical" className="h-6 mx-1" />

        {/* Theme toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={cycleTheme}
          aria-label={`Current theme: ${theme}. Click to change.`}
        >
          <ThemeIcon className="h-5 w-5" />
        </Button>

        <Separator orientation="vertical" className="h-6 mx-1" />

        {/* Notifications */}
        <NotificationBell />

        {/* Logout */}
        <Button
          variant="ghost"
          size="icon"
          aria-label="Logout"
          onClick={async () => { await logout(); navigate('/login'); }}
        >
          <LogOut className="h-5 w-5" />
        </Button>

        {/* Avatar */}
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-semibold text-white">
          {user?.username?.[0]?.toUpperCase() ?? 'W'}
        </div>
      </div>
    </header>
  );
}

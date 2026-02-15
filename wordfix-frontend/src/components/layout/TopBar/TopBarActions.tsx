import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, Monitor, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { useTheme } from '@/hooks/useTheme';
import { useAuthStore } from '@/stores/useAuthStore';
import { LevelProgress } from '@/features/progress/components/LevelProgress';
import { StreakWidget } from '@/features/review/components/StreakWidget';
import { NotificationBell } from '@/features/progress/components/NotificationBell';

const themeIcons = { light: Sun, dark: Moon, system: Monitor } as const;
const themeOrder = ['light', 'dark', 'system'] as const;

interface TopBarActionsProps {
  isDesktop: boolean;
}

export function TopBarActions({ isDesktop }: TopBarActionsProps) {
  const { theme, setTheme } = useTheme();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  const cycleTheme = () => {
    const idx = themeOrder.indexOf(theme as (typeof themeOrder)[number]);
    setTheme(themeOrder[(idx + 1) % 3]);
  };

  const ThemeIcon = themeIcons[theme as keyof typeof themeIcons] ?? Sun;

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="flex items-center gap-1">
      {isDesktop && (
        <>
          <LevelProgress compact />
          <StreakWidget compact />
          <Separator orientation="vertical" className="mx-1 h-5" />
        </>
      )}

      {/* Theme toggle */}
      <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground" onClick={cycleTheme}>
        <AnimatePresence mode="wait">
          <motion.div key={theme} initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.15 }}>
            <ThemeIcon size={16} />
          </motion.div>
        </AnimatePresence>
      </Button>

      {/* Notifications */}
      <NotificationBell />

      <Separator orientation="vertical" className="mx-1 h-5" />

      {/* Logout */}
      <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive" onClick={handleLogout}>
        <LogOut size={16} />
      </Button>

      {/* Avatar */}
      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary ring-2 ring-background transition-all hover:ring-primary/20">
        {user?.username?.[0]?.toUpperCase() ?? 'W'}
      </div>
    </div>
  );
}

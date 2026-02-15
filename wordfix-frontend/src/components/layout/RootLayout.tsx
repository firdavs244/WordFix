import { Outlet } from 'react-router-dom';
import TopBar from './TopBar/index';
import Sidebar from './Sidebar/index';
import { MobileNav } from './MobileNav';
import { HealthBanner } from './HealthBanner';
import { useMediaQuery } from '@/hooks/useMediaQuery';
import { useAppStore } from '@/stores/useAppStore';

export function RootLayout() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed);

  return (
    <div className="min-h-screen bg-background">
      <HealthBanner />
      <TopBar />
      {isDesktop && <Sidebar />}

      {isDesktop ? (
        <main
          className="pt-14 transition-all duration-300"
          style={{ marginLeft: sidebarCollapsed ? 68 : 260 }}
        >
          <div className="mx-auto max-w-7xl px-6 py-6">
            <Outlet />
          </div>
        </main>
      ) : (
        <main className="pt-14 pb-20">
          <div className="px-4 py-4">
            <Outlet />
          </div>
        </main>
      )}

      {!isDesktop && <MobileNav />}
    </div>
  );
}

import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { MobileNav } from './MobileNav';
import { HealthBanner } from '@/features/system/components/HealthBanner';
import { useMediaQuery } from '@/hooks/useMediaQuery';

/**
 * Root layout for authenticated pages.
 *
 * Desktop: TopBar + Sidebar + Main Content
 * Mobile: TopBar + Main Content + Bottom Navigation
 */
export function RootLayout() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-background">
      <TopBar />
      <HealthBanner />
      <div className="flex flex-1 overflow-hidden">
        {isDesktop && <Sidebar />}
        <main className="flex-1 overflow-y-auto p-4 pb-20 lg:p-6 lg:pb-6 scrollbar-thin">
          <Outlet />
        </main>
      </div>
      {!isDesktop && <MobileNav />}
    </div>
  );
}

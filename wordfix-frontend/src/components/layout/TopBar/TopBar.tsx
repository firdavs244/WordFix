import { useMediaQuery } from '@/hooks/useMediaQuery';
import { useAppStore } from '@/stores/useAppStore';
import { Logo } from '@/components/shared';
import { SearchBar } from './SearchBar';
import { TopBarActions } from './TopBarActions';

export default function TopBar() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed);
  const sidebarWidth = sidebarCollapsed ? 68 : 260;

  return (
    <header
      className="fixed top-0 right-0 z-40 flex h-14 items-center justify-between border-b border-border/40 px-4 glass lg:px-6"
      style={isDesktop ? { left: sidebarWidth } : { left: 0 }}
    >
      {isDesktop ? (
        <SearchBar />
      ) : (
        <Logo size="sm" />
      )}
      <TopBarActions isDesktop={isDesktop} />
    </header>
  );
}

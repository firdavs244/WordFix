import { motion } from 'framer-motion';
import { useAppStore } from '@/stores/useAppStore';
import { Separator } from '@/components/ui/separator';
import { SidebarLogo } from './SidebarLogo';
import { SidebarNav } from './SidebarNav';
import { SidebarToggle } from './SidebarToggle';

const sidebarSpring = { type: 'spring' as const, stiffness: 300, damping: 30 };

export default function Sidebar() {
  const { sidebarCollapsed, toggleSidebar } = useAppStore();
  const width = sidebarCollapsed ? 68 : 260;

  return (
    <motion.aside
      className="fixed left-0 top-0 z-30 flex h-screen flex-col border-r border-sidebar-border bg-sidebar py-4"
      animate={{ width }}
      transition={sidebarSpring}
    >
      <SidebarLogo collapsed={sidebarCollapsed} />
      <Separator className="my-3 mx-4 opacity-50" />
      <SidebarNav collapsed={sidebarCollapsed} />
      <div className="mt-auto">
        <SidebarToggle collapsed={sidebarCollapsed} onToggle={toggleSidebar} />
      </div>
    </motion.aside>
  );
}

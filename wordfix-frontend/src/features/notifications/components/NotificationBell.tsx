import { Bell } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useNotifications } from '../hooks/useNotifications';
import { NotificationPanel } from './NotificationPanel';

export function NotificationBell() {
  const {
    notifications,
    unreadCount,
    isLoading,
    isPanelOpen,
    togglePanel,
    closePanel,
    markRead,
    markAllRead,
  } = useNotifications();

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="icon"
        onClick={togglePanel}
        className="relative"
        aria-label={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ''}`}
      >
        <Bell className="h-5 w-5" />

        <AnimatePresence>
          {unreadCount > 0 && (
            <motion.span
              key="badge"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0 }}
              className="absolute -right-0.5 -top-0.5 flex h-4 min-w-[1rem] items-center justify-center rounded-full bg-destructive px-1 text-[10px] font-bold text-destructive-foreground"
            >
              {unreadCount > 99 ? '99+' : unreadCount}
            </motion.span>
          )}
        </AnimatePresence>
      </Button>

      <NotificationPanel
        isOpen={isPanelOpen}
        notifications={notifications}
        unreadCount={unreadCount}
        isLoading={isLoading}
        onClose={closePanel}
        onMarkRead={(id) => markRead(id)}
        onMarkAllRead={() => markAllRead()}
      />
    </div>
  );
}

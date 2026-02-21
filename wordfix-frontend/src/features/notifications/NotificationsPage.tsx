import { motion } from 'framer-motion';
import { pageTransition } from '@/lib/motion';
import PageHeader from '@/components/shared/PageHeader';
import { NotificationList } from './components/NotificationList';
import { Button } from '@/components/ui/button';
import { CheckCheck } from 'lucide-react';
import { useNotifications } from './hooks/useNotifications';

export function NotificationsPage() {
  const { notifications, unreadCount, isLoading, markRead, markAllRead } =
    useNotifications();

  return (
    <motion.div {...pageTransition} className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <PageHeader
          title="Notifications"
          description="Stay up to date with your learning journey"
        />
        {unreadCount > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => markAllRead()}
            className="gap-1.5"
          >
            <CheckCheck className="h-4 w-4" />
            Mark all read
          </Button>
        )}
      </div>

      <div className="rounded-xl border bg-card p-4 shadow-sm">
        <NotificationList
          notifications={notifications}
          isLoading={isLoading}
          onMarkRead={(id) => markRead(id)}
        />
      </div>
    </motion.div>
  );
}

export default NotificationsPage;

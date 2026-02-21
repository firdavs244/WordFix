import { motion, AnimatePresence } from 'framer-motion';
import { staggerContainer } from '@/lib/motion';
import type { NotificationData } from '@/types/notification';
import { NotificationItem } from './NotificationItem';
import EmptyState from '@/components/shared/EmptyState';
import { Bell } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';

interface Props {
  notifications: NotificationData[];
  isLoading: boolean;
  onMarkRead: (id: string) => void;
}

export function NotificationList({
  notifications,
  isLoading,
  onMarkRead,
}: Props) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="flex items-start gap-3 p-3">
            <Skeleton className="h-9 w-9 rounded-full" />
            <div className="flex-1 space-y-1.5">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-full" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (notifications.length === 0) {
    return (
      <EmptyState
        icon={Bell}
        title="No notifications yet"
        description="You're all caught up!"
      />
    );
  }

  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      role="list"
      className="space-y-1"
    >
      <AnimatePresence mode="popLayout">
        {notifications.map((n) => (
          <NotificationItem
            key={n.id}
            notification={n}
            onMarkRead={onMarkRead}
          />
        ))}
      </AnimatePresence>
    </motion.div>
  );
}

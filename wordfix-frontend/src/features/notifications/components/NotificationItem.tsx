import { motion } from 'framer-motion';
import type { NotificationData } from '@/types/notification';
import { NotificationTypeIcon } from './NotificationTypeIcon';
import { NotificationTimeAgo } from './NotificationTimeAgo';

interface Props {
  notification: NotificationData;
  onMarkRead: (id: string) => void;
}

export function NotificationItem({ notification, onMarkRead }: Props) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className={`flex items-start gap-3 rounded-lg p-3 transition-colors ${
        notification.is_read
          ? 'opacity-60'
          : 'bg-primary/5 hover:bg-primary/10'
      }`}
      role="listitem"
    >
      <NotificationTypeIcon type={notification.type} />

      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium leading-tight">
          {notification.title}
        </p>
        <p className="mt-0.5 text-xs text-muted-foreground line-clamp-2">
          {notification.message}
        </p>
        <NotificationTimeAgo date={notification.created_at} />
      </div>

      {!notification.is_read && (
        <button
          onClick={() => onMarkRead(notification.id)}
          className="mt-1 h-2 w-2 shrink-0 rounded-full bg-primary"
          aria-label={`Mark "${notification.title}" as read`}
        />
      )}
    </motion.div>
  );
}

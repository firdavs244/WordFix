import { motion, AnimatePresence } from 'framer-motion';
import { CheckCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { NotificationList } from './NotificationList';
import type { NotificationData } from '@/types/notification';

interface Props {
  isOpen: boolean;
  notifications: NotificationData[];
  unreadCount: number;
  isLoading: boolean;
  onClose: () => void;
  onMarkRead: (id: string) => void;
  onMarkAllRead: () => void;
}

export function NotificationPanel({
  isOpen,
  notifications,
  unreadCount,
  isLoading,
  onClose,
  onMarkRead,
  onMarkAllRead,
}: Props) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Panel */}
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ type: 'spring', stiffness: 400, damping: 30 }}
            className="absolute right-0 top-full z-50 mt-2 w-96 overflow-hidden rounded-xl border bg-card shadow-xl"
          >
            {/* Header */}
            <div className="flex items-center justify-between border-b px-4 py-3">
              <h3 className="text-sm font-semibold">Notifications</h3>
              {unreadCount > 0 && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onMarkAllRead}
                  className="h-7 gap-1 text-xs"
                >
                  <CheckCheck className="h-3.5 w-3.5" />
                  Mark all read
                </Button>
              )}
            </div>

            {/* List */}
            <div className="max-h-[28rem] overflow-y-auto p-2">
              <NotificationList
                notifications={notifications}
                isLoading={isLoading}
                onMarkRead={onMarkRead}
              />
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

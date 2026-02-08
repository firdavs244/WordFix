import { useState } from 'react';
import { motion } from 'framer-motion';
import { Bell, CheckCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import {
  useNotifications,
  useMarkNotificationRead,
  useMarkAllNotificationsRead,
} from '../hooks/useProgress';
import { listContainerVariants, listItemVariants } from '@/components/animations/PageTransition';
import { cn } from '@/lib/utils';
import type { NotificationData } from '@/types';

const typeIcons: Record<string, string> = {
  badge_earned: '🏆',
  level_up: '🎉',
  review_reminder: '📚',
  streak_warning: '🔥',
  daily_goal_complete: '✅',
  word_mastered: '⭐',
  weekly_report: '📊',
};

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

export function NotificationsPage() {
  const [page, setPage] = useState(1);
  const { data, isLoading } = useNotifications(page, 20);
  const markRead = useMarkNotificationRead();
  const markAllRead = useMarkAllNotificationsRead();

  const notifications = data?.data?.notifications ?? [];
  const unreadCount = data?.data?.unread_count ?? 0;
  const totalPages = data?.meta?.total_pages ?? 1;

  return (
    <PageTransition>
      <div className="mx-auto max-w-3xl space-y-6">
        <motion.div
          className="flex items-center justify-between"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10">
              <Bell className="h-6 w-6 text-primary" />
            </div>
            <div>
              <h1 className="font-heading text-3xl font-bold">Notifications</h1>
              <p className="text-muted-foreground">
                {unreadCount > 0 ? `${unreadCount} unread` : 'All caught up!'}
              </p>
            </div>
          </div>
          {unreadCount > 0 && (
            <Button variant="outline" onClick={() => markAllRead.mutate()} className="gap-2">
              <CheckCheck className="h-4 w-4" />
              Mark all read
            </Button>
          )}
        </motion.div>

        {isLoading ? (
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <Card key={i} className="border-border/50">
                <CardContent className="p-4">
                  <div className="h-12 animate-pulse rounded bg-muted" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : notifications.length === 0 ? (
          <Card className="border-border/50">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Bell className="h-12 w-12 text-muted-foreground/30" />
              <p className="mt-4 text-muted-foreground">No notifications yet</p>
            </CardContent>
          </Card>
        ) : (
          <motion.div
            className="space-y-2"
            variants={listContainerVariants}
            initial="hidden"
            animate="show"
          >
            {notifications.map((n: NotificationData) => (
              <motion.div key={n.id} variants={listItemVariants}>
                <Card
                  className={cn(
                    'cursor-pointer border-border/50 transition-colors',
                    !n.is_read && 'border-l-4 border-l-primary bg-primary/5',
                  )}
                  onClick={() => {
                    if (!n.is_read) markRead.mutate(n.id);
                  }}
                >
                  <CardContent className="flex items-start gap-3 p-4">
                    <span className="mt-0.5 text-xl">
                      {typeIcons[n.type] ?? '📩'}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className={cn('text-sm', !n.is_read && 'font-semibold')}>
                        {n.title}
                      </p>
                      <p className="mt-0.5 text-sm text-muted-foreground">{n.message}</p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        {formatDate(n.created_at)}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-center gap-2">
            <Button
              variant="outline"
              size="sm"
              disabled={page <= 1}
              onClick={() => setPage((p) => p - 1)}
            >
              Previous
            </Button>
            <span className="text-sm text-muted-foreground">
              Page {page} of {totalPages}
            </span>
            <Button
              variant="outline"
              size="sm"
              disabled={page >= totalPages}
              onClick={() => setPage((p) => p + 1)}
            >
              Next
            </Button>
          </div>
        )}
      </div>
    </PageTransition>
  );
}

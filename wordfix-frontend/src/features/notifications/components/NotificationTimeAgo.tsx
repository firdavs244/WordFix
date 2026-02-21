import { formatDistanceToNow } from 'date-fns';

interface Props {
  date: string;
}

export function NotificationTimeAgo({ date }: Props) {
  const ago = formatDistanceToNow(new Date(date), { addSuffix: true });

  return (
    <span className="text-xs text-muted-foreground" title={date}>
      {ago}
    </span>
  );
}

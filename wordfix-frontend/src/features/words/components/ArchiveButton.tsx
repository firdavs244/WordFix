import { Archive, ArchiveRestore } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ArchiveButtonProps {
  isArchived: boolean;
  onArchive: () => void;
  onUnarchive: () => void;
  isLoading?: boolean;
  size?: 'sm' | 'icon';
  className?: string;
}

export function ArchiveButton({ isArchived, onArchive, onUnarchive, isLoading, size = 'sm', className }: ArchiveButtonProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    isArchived ? onUnarchive() : onArchive();
  };

  if (size === 'icon') {
    return (
      <Button
        variant="ghost"
        size="icon"
        className={cn('h-8 w-8', className)}
        onClick={handleClick}
        disabled={isLoading}
        title={isArchived ? 'Unarchive' : 'Archive'}
      >
        {isArchived ? (
          <ArchiveRestore className="h-4 w-4 text-muted-foreground hover:text-primary" />
        ) : (
          <Archive className="h-4 w-4 text-muted-foreground hover:text-warning-foreground" />
        )}
      </Button>
    );
  }

  return (
    <Button
      variant={isArchived ? 'outline' : 'secondary'}
      size="sm"
      className={cn('gap-1.5', className)}
      onClick={handleClick}
      disabled={isLoading}
    >
      {isArchived ? (
        <>
          <ArchiveRestore className="h-3.5 w-3.5" />
          Unarchive
        </>
      ) : (
        <>
          <Archive className="h-3.5 w-3.5" />
          Archive
        </>
      )}
    </Button>
  );
}

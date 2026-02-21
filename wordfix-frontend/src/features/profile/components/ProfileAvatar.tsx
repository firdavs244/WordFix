import { cn } from '@/lib/utils';

interface ProfileAvatarProps {
  name: string;
  size?: 'sm' | 'md' | 'lg';
}

const sizes = { sm: 'h-10 w-10', md: 'h-16 w-16', lg: 'h-20 w-20' };
const textSizes = { sm: 'text-base', md: 'text-xl', lg: 'text-2xl' };

export default function ProfileAvatar({ name, size = 'md' }: ProfileAvatarProps) {
  const letter = name?.charAt(0)?.toUpperCase() || '?';

  return (
    <div
      className={cn(
        'rounded-full border-4 border-background bg-gradient-to-br from-primary/20 to-secondary/20 shadow-lg flex items-center justify-center',
        sizes[size],
      )}
    >
      <span className={cn('font-heading font-bold text-primary', textSizes[size])}>{letter}</span>
    </div>
  );
}

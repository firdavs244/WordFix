import { SkipForward } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface SkipButtonProps {
  onSkip: () => void;
  isLoading?: boolean;
}

export function SkipButton({ onSkip, isLoading = false }: SkipButtonProps) {
  return (
    <Button
      variant="ghost"
      size="sm"
      className="gap-1.5 text-muted-foreground hover:text-foreground"
      onClick={onSkip}
      disabled={isLoading}
    >
      <SkipForward className="h-4 w-4" />
      {isLoading ? 'Skipping...' : 'Skip for now'}
    </Button>
  );
}

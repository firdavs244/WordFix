import { useNavigate } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { AlertTriangle } from 'lucide-react';

interface ConfusingPairBadgeProps {
  confusingWith?: string;
}

export function ConfusingPairBadge({ confusingWith }: ConfusingPairBadgeProps) {
  const navigate = useNavigate();

  if (!confusingWith) return null;

  return (
    <Badge
      variant="outline"
      className="cursor-pointer gap-1 bg-amber-500/10 text-amber-600 hover:bg-amber-500/20 dark:text-amber-400"
      onClick={(e) => {
        e.stopPropagation();
        navigate('/confusing-pairs');
      }}
    >
      <AlertTriangle className="h-3 w-3" />
      Often confused with: {confusingWith}
    </Badge>
  );
}

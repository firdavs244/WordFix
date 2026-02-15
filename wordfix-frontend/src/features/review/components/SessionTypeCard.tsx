import { motion } from 'framer-motion';
import { ArrowRight, type LucideIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { bounceIn, staggerItem } from '@/lib/motion';
import MouseTiltCard from '@/features/dashboard/components/MouseTiltCard';
import { useStartSession } from '../hooks/useReview';
import type { SessionType } from '@/types';
import { cn } from '@/lib/utils';

interface Props {
  type: SessionType;
  title: string;
  description: string;
  icon: LucideIcon;
  gradient: string;
  iconGradient: string;
  count?: number;
  disabled?: boolean;
}

export default function SessionTypeCard({ type, title, description, icon: Icon, gradient, iconGradient, count, disabled }: Props) {
  const navigate = useNavigate();
  const startSession = useStartSession();

  const handleClick = async () => {
    if (disabled) return;
    try {
      const res = await startSession.mutateAsync(type);
      navigate(`/review/session/${res.data.id}`, { state: { sessionType: type } });
    } catch { /* handled */ }
  };

  return (
    <motion.div variants={staggerItem}>
      <MouseTiltCard tiltAmount={3} glare>
        <div
          onClick={handleClick}
          role="button"
          aria-disabled={disabled}
          className={cn(
            'relative cursor-pointer overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br p-6 shadow-card transition-all hover:border-border hover:shadow-card-hover',
            gradient,
            disabled && 'cursor-not-allowed opacity-50',
          )}
        >
          <motion.div variants={bounceIn} className={cn('mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br shadow-lg', iconGradient)}>
            <Icon className="h-7 w-7 text-white" />
          </motion.div>
          <h3 className="font-heading text-base font-semibold">{title}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{description}</p>
          {count !== undefined && (
            <span className="mt-3 inline-flex rounded-full bg-card/80 px-2.5 py-1 text-xs">{count} words</span>
          )}
          <ArrowRight className="absolute bottom-6 right-6 h-4 w-4 text-muted-foreground/30 transition-transform group-hover:translate-x-1" />
        </div>
      </MouseTiltCard>
    </motion.div>
  );
}

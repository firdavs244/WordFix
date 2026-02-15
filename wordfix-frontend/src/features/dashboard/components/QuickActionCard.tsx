import { Link } from 'react-router-dom';
import { ArrowRight, type LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';
import MouseTiltCard from './MouseTiltCard';

interface QuickActionCardProps {
  title: string;
  description: string;
  icon: LucideIcon;
  href: string;
  gradient: string;
  iconColor: string;
}

export default function QuickActionCard({
  title,
  description,
  icon: Icon,
  href,
  gradient,
  iconColor,
}: QuickActionCardProps) {
  return (
    <Link to={href}>
      <MouseTiltCard tiltAmount={2}>
        <div
          className={cn(
            'group relative overflow-hidden rounded-2xl border border-border/50 p-5 shadow-card transition-all duration-200',
            `bg-gradient-to-br ${gradient}`,
            'hover:border-primary/20',
          )}
        >
          {/* Decorative large background icon */}
          <Icon className="pointer-events-none absolute -bottom-4 -right-4 h-20 w-20 opacity-[0.04]" />

          <div className="relative z-10 flex items-center gap-4">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-border/30 bg-card/80 shadow-sm">
              <Icon className={cn('h-[22px] w-[22px]', iconColor)} />
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-heading font-semibold">{title}</h4>
              <p className="mt-0.5 text-xs text-muted-foreground">{description}</p>
            </div>
            <ArrowRight className="h-4 w-4 text-muted-foreground/30 transition-all duration-200 group-hover:translate-x-[3px] group-hover:text-foreground" />
          </div>
        </div>
      </MouseTiltCard>
    </Link>
  );
}

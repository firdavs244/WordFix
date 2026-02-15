import { Link } from 'react-router-dom';
import { Trophy, ArrowRight, type LucideIcon } from 'lucide-react';
import MouseTiltCard from '@/features/dashboard/components/MouseTiltCard';

interface Props {
  id: string;
  title: string;
  description: string;
  icon: LucideIcon;
  gradient: string;
  iconGradient: string;
  route: string;
  bestScore?: number;
}

export default function GameCard({ title, description, icon: Icon, gradient, iconGradient, route, bestScore }: Props) {
  return (
    <MouseTiltCard tiltAmount={3} glare>
      <Link to={route} className="block">
        <div className={`relative overflow-hidden rounded-2xl border border-border/50 bg-gradient-to-br ${gradient} p-6 shadow-card`}>
          <Icon className="absolute bottom-2 right-2 h-20 w-20 opacity-[0.05]" />
          <div className={`mb-4 flex h-[52px] w-[52px] items-center justify-center rounded-2xl bg-gradient-to-br ${iconGradient} shadow-lg`}>
            <Icon className="h-[26px] w-[26px] text-white" />
          </div>
          <h3 className="font-heading text-base font-semibold">{title}</h3>
          <p className="mt-1 text-sm text-muted-foreground">{description}</p>
          {bestScore !== undefined && (
            <div className="mt-3 flex items-center gap-1.5">
              <Trophy className="h-3 w-3 text-accent" />
              <span className="text-xs font-medium text-accent">Best: {bestScore}%</span>
            </div>
          )}
          <ArrowRight className="absolute bottom-6 right-6 h-4 w-4 text-muted-foreground" />
        </div>
      </Link>
    </MouseTiltCard>
  );
}

import { motion } from 'framer-motion';
import { Gauge } from 'lucide-react';
import { AnimatedCounter } from '@/components/shared';
import { progressFill } from '@/lib/motion';
import { useDashboardData } from '../hooks/useDashboardData';

export default function AverageConfidenceBar() {
  const { stats } = useDashboardData();
  const confidence = Math.round(stats?.average_confidence ?? 0);

  return (
    <div className="flex items-center gap-4 rounded-xl border border-border/50 bg-card p-4 shadow-card">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary/10">
        <Gauge className="h-[18px] w-[18px] text-primary" />
      </div>

      <div className="flex-1">
        <p className="text-sm font-medium">Average Confidence</p>
        <div className="relative mt-1.5 h-2.5 overflow-hidden rounded-full bg-muted">
          <motion.div
            className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-primary to-secondary"
            {...progressFill(confidence, 0.3)}
            style={{ boxShadow: 'inset 0 1px 2px rgba(255,255,255,0.15)' }}
          />
        </div>
      </div>

      <p className="text-xl font-heading font-bold text-primary">
        <AnimatedCounter value={confidence} suffix="%" />
      </p>
    </div>
  );
}

import { motion } from 'framer-motion';
import { Sparkles } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { Skeleton } from '@/components/ui/skeleton';
import { useWordRecommendations } from '@/features/learning-profile/hooks/useLearning';
import RecommendationItem from './RecommendationItem';

export default function RecommendationsWidget() {
  const { data, isLoading } = useWordRecommendations();
  const recommendations = data?.data ?? [];

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 shadow-card">
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <Skeleton key={i} className="h-14 rounded-xl" />)}
        </div>
      </div>
    );
  }

  const items = Array.isArray(recommendations) ? recommendations.slice(0, 3) : [];

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center gap-2 px-5 pt-5">
        <Sparkles className="h-[18px] w-[18px] text-accent" />
        <h3 className="text-base font-heading font-semibold">Tavsiya qilingan so'zlar</h3>
      </div>

      {items.length === 0 ? (
        <p className="px-5 py-8 text-center text-sm text-muted-foreground">
          Hozircha tavsiyalar yo'q
        </p>
      ) : (
        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="space-y-1.5 px-5 py-4"
        >
          {items.map((rec: any) => (
            <RecommendationItem key={rec.id} recommendation={rec} />
          ))}
        </motion.div>
      )}
    </div>
  );
}

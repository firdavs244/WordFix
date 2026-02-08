import { motion } from 'framer-motion';
import { Award } from 'lucide-react';
import { PageTransition } from '@/components/animations/PageTransition';
import { BadgeGrid } from '../components/BadgeGrid';

export function BadgesPage() {
  return (
    <PageTransition>
      <div className="mx-auto max-w-5xl space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-500/10">
              <Award className="h-6 w-6 text-amber-500" />
            </div>
            <div>
              <h1 className="font-heading text-3xl font-bold">Badges</h1>
              <p className="text-muted-foreground">Earn badges by completing activities</p>
            </div>
          </div>
        </motion.div>

        <BadgeGrid />
      </div>
    </PageTransition>
  );
}

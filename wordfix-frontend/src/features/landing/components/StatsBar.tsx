import { motion } from 'framer-motion';
import { BookOpen, Users, TrendingUp } from 'lucide-react';
import { staggerContainer, staggerItem } from '@/lib/motion';

const stats = [
  { number: '10,000+', label: 'Words Learned', icon: BookOpen },
  { number: '500+', label: 'Active Learners', icon: Users },
  { number: '95%', label: 'Retention Rate', icon: TrendingUp },
];

export function StatsBar() {
  return (
    <section className="px-6 py-16 lg:py-20">
      <motion.div
        variants={staggerContainer}
        initial="initial"
        whileInView="animate"
        viewport={{ once: true, amount: 0.3 }}
        className="mx-auto grid max-w-4xl grid-cols-3 gap-8 lg:gap-16"
      >
        {stats.map((s) => (
          <motion.div key={s.label} variants={staggerItem} className="text-center">
            <s.icon className="mx-auto h-5 w-5 text-primary/40" />
            <p className="mt-2 font-heading text-3xl font-bold lg:text-4xl">{s.number}</p>
            <p className="mt-1 text-sm text-muted-foreground">{s.label}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}

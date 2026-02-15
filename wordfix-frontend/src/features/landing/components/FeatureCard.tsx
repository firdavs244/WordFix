import { motion } from 'framer-motion';
import { type LucideIcon } from 'lucide-react';
import { staggerItem } from '@/lib/motion';

interface Props {
  icon: LucideIcon;
  iconGradient: string;
  title: string;
  description: string;
}

export function FeatureCard({ icon: Icon, iconGradient, title, description }: Props) {
  return (
    <motion.div variants={staggerItem} className="group relative overflow-hidden rounded-2xl border border-border/50 bg-card p-7 shadow-card transition-all duration-300 hover:shadow-card-hover lg:p-8">
      {/* Faded bg icon */}
      <Icon className="absolute -bottom-6 -right-6 h-[100px] w-[100px] opacity-[0.03]" />

      <motion.div
        className={`flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br ${iconGradient} shadow-lg`}
        initial={{ scale: 0 }}
        whileInView={{ scale: 1 }}
        viewport={{ once: true }}
        transition={{ type: 'spring', stiffness: 200, damping: 12 }}
      >
        <Icon className="h-7 w-7 text-white" />
      </motion.div>

      <h3 className="mt-5 font-heading text-lg font-semibold">{title}</h3>
      <p className="mt-2.5 text-sm leading-relaxed text-muted-foreground">{description}</p>
    </motion.div>
  );
}

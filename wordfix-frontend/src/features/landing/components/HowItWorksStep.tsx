import { motion } from 'framer-motion';
import { type LucideIcon } from 'lucide-react';
import { staggerItem, bounceIn } from '@/lib/motion';

interface Props {
  number: number;
  icon: LucideIcon;
  title: string;
  description: string;
}

export function HowItWorksStep({ number, icon: Icon, title, description }: Props) {
  return (
    <motion.div variants={staggerItem} className="text-center">
      <motion.div
        className="mx-auto flex h-8 w-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-white"
        initial="initial"
        whileInView="animate"
        viewport={{ once: true }}
        variants={bounceIn}
      >
        {number}
      </motion.div>
      <div className="mx-auto mt-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-muted/50">
        <Icon className="h-6 w-6 text-foreground" />
      </div>
      <h3 className="mt-4 font-heading text-base font-semibold">{title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{description}</p>
    </motion.div>
  );
}

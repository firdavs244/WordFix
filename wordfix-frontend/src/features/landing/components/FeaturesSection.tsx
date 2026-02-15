import { motion } from 'framer-motion';
import { Brain, Repeat, Gamepad2 } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { GradientText } from '@/components/shared';
import { FeatureCard } from './FeatureCard';

const features = [
  {
    icon: Brain,
    iconGradient: 'from-primary to-violet-500',
    title: 'AI-Powered Adaptation',
    description: 'Our AI analyzes your learning patterns, identifies weaknesses, and creates personalized study plans that evolve with you.',
  },
  {
    icon: Repeat,
    iconGradient: 'from-secondary to-cyan-400',
    title: 'Smart Spaced Repetition',
    description: 'Scientifically-proven SRS algorithm shows you words at the perfect moment for maximum long-term retention.',
  },
  {
    icon: Gamepad2,
    iconGradient: 'from-accent to-orange-400',
    title: 'Gamified Learning',
    description: 'XP points, streaks, daily challenges, 5 game modes, and achievements make vocabulary building genuinely fun.',
  },
];

export function FeaturesSection() {
  return (
    <section className="relative bg-muted/20 px-6 py-24 lg:py-32">
      <div className="mx-auto max-w-6xl">
        <p className="text-center text-xs font-semibold uppercase tracking-widest text-primary">Powered by Science</p>
        <h2 className="mt-2 text-center font-heading text-3xl font-bold lg:text-4xl">
          Everything You Need to <GradientText>Master Vocabulary</GradientText>
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-muted-foreground">
          Built on proven learning science, enhanced with modern AI technology.
        </p>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, amount: 0.2 }}
          className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-3 lg:gap-8"
        >
          {features.map((f) => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </motion.div>
      </div>
    </section>
  );
}

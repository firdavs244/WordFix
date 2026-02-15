import { motion } from 'framer-motion';
import { Upload, Brain, Gamepad2, Trophy, ArrowRight } from 'lucide-react';
import { staggerContainer } from '@/lib/motion';
import { HowItWorksStep } from './HowItWorksStep';

const steps = [
  { number: 1, icon: Upload, title: 'Add Words', description: 'Import from text, CSV, or add manually. AI enriches with translations, examples, and mnemonics.' },
  { number: 2, icon: Brain, title: 'AI Analyzes', description: 'Our AI determines difficulty, identifies patterns, and creates your personalized study plan.' },
  { number: 3, icon: Gamepad2, title: 'Practice & Play', description: 'Review with smart flashcards, take AI tests, play 5 game modes, chat with AI tutor.' },
  { number: 4, icon: Trophy, title: 'Master & Grow', description: 'Track progress, earn badges, climb levels, and achieve lasting vocabulary mastery.' },
];

export function HowItWorksSection() {
  return (
    <section className="px-6 py-24 lg:py-32">
      <div className="mx-auto max-w-5xl">
        <p className="text-center text-xs font-semibold uppercase tracking-widest text-primary">Simple as 1-2-3-4</p>
        <h2 className="mt-2 text-center font-heading text-3xl font-bold lg:text-4xl">How It Works</h2>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, amount: 0.2 }}
          className="mt-16 grid grid-cols-1 gap-8 md:grid-cols-4"
        >
          {steps.map((s, i) => (
            <div key={s.number} className="flex items-center gap-4 md:flex-col md:gap-0">
              <HowItWorksStep {...s} />
              {i < steps.length - 1 && (
                <ArrowRight className="hidden h-4 w-4 text-muted-foreground/20 md:block" style={{ marginTop: '-2rem' }} />
              )}
            </div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

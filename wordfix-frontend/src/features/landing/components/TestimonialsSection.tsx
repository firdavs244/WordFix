import { motion } from 'framer-motion';
import { staggerContainer, staggerItem } from '@/lib/motion';

const testimonials = [
  {
    quote: 'WordFix transformed how I learn English. The spaced repetition actually works — I remember words effortlessly now.',
    name: 'Aziza M.',
    role: 'Student',
    initial: 'A',
  },
  {
    quote: 'The gamification keeps me coming back every day. My 45-day streak is my proudest achievement!',
    name: 'Jasur K.',
    role: 'Developer',
    initial: 'J',
  },
  {
    quote: 'As a teacher, I recommend WordFix to all my students. The AI adaptation is genuinely impressive.',
    name: 'Nilufar T.',
    role: 'English Teacher',
    initial: 'N',
  },
];

export function TestimonialsSection() {
  return (
    <section className="bg-muted/20 px-6 py-24">
      <div className="mx-auto max-w-5xl">
        <h2 className="text-center font-heading text-3xl font-bold">Loved by Learners</h2>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          whileInView="animate"
          viewport={{ once: true, amount: 0.2 }}
          className="mt-12 grid grid-cols-1 gap-6 md:grid-cols-3"
        >
          {testimonials.map((t) => (
            <motion.div key={t.name} variants={staggerItem} className="rounded-2xl border border-border/50 bg-card p-6 shadow-card">
              <p className="text-sm italic leading-relaxed text-muted-foreground">&ldquo;{t.quote}&rdquo;</p>
              <div className="mt-4 flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-secondary/20">
                  <span className="text-sm font-semibold text-primary">{t.initial}</span>
                </div>
                <div>
                  <p className="text-sm font-medium">{t.name}</p>
                  <p className="text-xs text-muted-foreground">{t.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}

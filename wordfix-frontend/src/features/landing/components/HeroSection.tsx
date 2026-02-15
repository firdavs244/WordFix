import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { fadeInUp } from '@/lib/motion';
import { GradientText } from '@/components/shared';
import { HeroVisual } from './HeroVisual';

export function HeroSection() {
  return (
    <section className="relative flex min-h-[90vh] items-center justify-center overflow-hidden px-6 pb-16 pt-24">
      {/* Gradient orbs */}
      <div className="pointer-events-none absolute -left-20 -top-20 h-[500px] w-[500px] animate-float rounded-full bg-primary/[0.15] blur-[120px]" />
      <div className="pointer-events-none absolute bottom-0 right-10 h-[400px] w-[400px] animate-float rounded-full bg-secondary/10 blur-[100px]" style={{ animationDelay: '-3s', animationDuration: '12s' }} />
      <div className="pointer-events-none absolute right-1/4 top-1/3 h-[300px] w-[300px] animate-float rounded-full bg-accent/10 blur-[80px]" style={{ animationDelay: '-6s', animationDuration: '18s' }} />
      {/* Grid pattern */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.03]" style={{ backgroundImage: 'radial-gradient(circle, currentColor 1px, transparent 1px)', backgroundSize: '30px 30px' }} />

      <div className="relative z-10 mx-auto grid max-w-5xl grid-cols-1 items-center gap-12 lg:grid-cols-2">
        {/* Text column */}
        <div>
          <motion.div variants={fadeInUp} initial="initial" animate="animate" className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-3 py-1.5 text-xs font-semibold text-primary">
            ✨ AI-Powered Vocabulary Learning
          </motion.div>
          <motion.h1 variants={fadeInUp} initial="initial" animate="animate" transition={{ delay: 0.1 }} className="mt-4 font-heading text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Master Every <GradientText>Word</GradientText>
            <br />with Confidence
          </motion.h1>
          <motion.p variants={fadeInUp} initial="initial" animate="animate" transition={{ delay: 0.2 }} className="mt-6 max-w-lg text-base leading-relaxed text-muted-foreground lg:text-lg">
            The intelligent vocabulary platform that adapts to your learning style. Build lasting word knowledge through AI-powered spaced repetition, gamified practice, and real conversations.
          </motion.p>

          <motion.div variants={fadeInUp} initial="initial" animate="animate" transition={{ delay: 0.3 }} className="mt-8 flex gap-4">
            <Link to="/register" className="group inline-flex h-12 items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 px-7 text-base font-semibold text-white shadow-lg shadow-primary/20 transition-all hover:scale-[1.02] hover:shadow-xl hover:shadow-primary/30">
              Start Learning Free <ArrowRight className="h-[18px] w-[18px] transition-transform group-hover:translate-x-0.5" />
            </Link>
            <Link to="/login" className="inline-flex h-12 items-center rounded-xl border border-border bg-card/50 px-7 font-medium backdrop-blur-sm transition hover:border-border/80 hover:bg-card">
              Sign In
            </Link>
          </motion.div>

          <motion.div variants={fadeInUp} initial="initial" animate="animate" transition={{ delay: 0.4 }} className="mt-6 flex items-center gap-3">
            {['bg-primary/10', 'bg-secondary/10', 'bg-accent/10'].map((bg, i) => (
              <div key={i} className={`h-7 w-7 rounded-full border-2 border-background ${bg} ${i > 0 ? '-ml-2' : ''}`} />
            ))}
            <span className="text-sm text-muted-foreground">Joined by 500+ learners</span>
          </motion.div>
        </div>

        {/* Visual column */}
        <div className="hidden lg:block">
          <HeroVisual />
        </div>
      </div>
    </section>
  );
}

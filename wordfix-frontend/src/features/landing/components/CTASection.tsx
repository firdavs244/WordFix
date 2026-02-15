import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { GradientText } from '@/components/shared';

export function CTASection() {
  return (
    <section className="relative px-6 py-24 lg:py-32">
      {/* Decorative orbs */}
      <div className="pointer-events-none absolute left-1/4 top-1/4 h-48 w-48 rounded-full bg-primary/10 blur-[80px]" />
      <div className="pointer-events-none absolute bottom-1/4 right-1/4 h-40 w-40 rounded-full bg-secondary/10 blur-[60px]" />

      <div className="relative z-10 mx-auto max-w-3xl text-center">
        <h2 className="font-heading text-3xl font-bold lg:text-4xl">
          Ready to Master <GradientText>Every Word</GradientText>?
        </h2>
        <p className="mx-auto mt-4 max-w-lg text-muted-foreground">
          Join hundreds of learners who are building powerful vocabularies with AI assistance. Start for free today.
        </p>
        <motion.div className="mt-8" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
          <Link
            to="/register"
            className="inline-flex h-14 items-center gap-2.5 rounded-2xl bg-gradient-to-r from-primary to-primary/90 px-10 text-lg font-semibold text-white shadow-lg shadow-primary/25 transition-shadow hover:shadow-xl hover:shadow-primary/35"
          >
            Start Learning — It&apos;s Free <ArrowRight className="h-5 w-5" />
          </Link>
        </motion.div>
        <p className="mt-3 text-xs text-muted-foreground/50">No credit card required</p>
      </div>
    </section>
  );
}

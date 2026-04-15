import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

const words = ['Architecture', 'Kubernetes', 'Microservices', 'Real-time'];

export default function Hero() {
  const [wordIndex, setWordIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setWordIndex((i) => (i + 1) % words.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
      {/* Animated background shapes */}
      <div className="absolute inset-0 pointer-events-none">
        <motion.div
          className="absolute w-72 h-72 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #3b82f6, transparent)', top: '10%', left: '10%' }}
          animate={{ y: [0, -30, 0], x: [0, 15, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute w-96 h-96 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #8b5cf6, transparent)', bottom: '10%', right: '10%' }}
          animate={{ y: [0, 20, 0], x: [0, -20, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute w-48 h-48 rounded-full opacity-8"
          style={{ background: 'radial-gradient(circle, #10b981, transparent)', top: '50%', right: '30%' }}
          animate={{ y: [0, -25, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 text-center"
      >
        <motion.div
          className="inline-block mb-6 px-4 py-2 rounded-full border border-[var(--color-border-glass)] text-sm text-[var(--color-text-secondary)]"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          10 Pods / 6 Deployments / 4 StatefulSets / k3s Cluster
        </motion.div>

        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 leading-tight">
          <span className="text-[var(--color-text-primary)]">WordFix</span>
          <br />
          <span className="gradient-text">
            <motion.span
              key={wordIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              {words[wordIndex]}
            </motion.span>
          </span>
        </h1>

        <motion.p
          className="text-lg md:text-xl text-[var(--color-text-secondary)] max-w-2xl mx-auto mb-10"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          A production-grade language learning platform built with microservices,
          deployed on Kubernetes. Explore the architecture, infrastructure, and
          request flow below.
        </motion.p>

        <motion.a
          href="#architecture"
          className="inline-flex items-center gap-2 px-8 py-3 rounded-full bg-gradient-to-r from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] text-white font-medium hover:shadow-lg hover:shadow-[var(--color-accent-purple)]/25 transition-shadow"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Explore Architecture
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
        </motion.a>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-10 left-1/2 -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-6 h-10 rounded-full border-2 border-[var(--color-text-muted)] flex items-start justify-center p-1">
          <motion.div
            className="w-1.5 h-3 rounded-full bg-[var(--color-text-muted)]"
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>
      </motion.div>
    </section>
  );
}

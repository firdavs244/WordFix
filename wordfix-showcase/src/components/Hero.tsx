import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';

const words = ['Arxitektura', 'Kubernetes', 'Mikroservislar', 'DDD'];

export default function Hero() {
  const [wordIndex, setWordIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setWordIndex((i) => (i + 1) % words.length), 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
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
          className="absolute w-48 h-48 rounded-full opacity-10"
          style={{ background: 'radial-gradient(circle, #10b981, transparent)', top: '50%', right: '30%' }}
          animate={{ y: [0, -25, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }} className="relative z-10 text-center max-w-4xl mx-auto">
        <motion.div
          className="inline-block mb-8 px-5 py-2.5 rounded-full border border-[var(--color-border-glass)] text-sm text-[var(--color-text-secondary)]"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          11 Pod / 7 Deployment / 4 StatefulSet / k3s Klaster
        </motion.div>

        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-8 leading-tight">
          <span className="text-[var(--color-text-primary)]">WordFix</span>
          <br />
          <span className="gradient-text">
            <motion.span key={wordIndex} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
              {words[wordIndex]}
            </motion.span>
          </span>
        </h1>

        <motion.p className="text-lg md:text-xl text-[var(--color-text-secondary)] max-w-2xl mx-auto mb-12" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}>
          Production-darajadagi til o'rganish platformasi. Mikroservis arxitektura,
          Kubernetes infratuzilma, DDD dizayn va so'rov oqimini quyida batafsil ko'ring.
        </motion.p>

        <motion.div className="flex flex-wrap justify-center gap-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.7 }}>
          <motion.a
            href="#architecture"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-gradient-to-r from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] text-white font-medium hover:shadow-lg hover:shadow-[var(--color-accent-purple)]/25 transition-shadow"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Arxitekturani Ko'rish
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
          </motion.a>
          <motion.a
            href="#ddd"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full border border-[var(--color-border-glass)] text-[var(--color-text-secondary)] hover:text-white hover:border-[var(--color-accent-purple)] transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            DDD Strukturasi
          </motion.a>
        </motion.div>
      </motion.div>

      <motion.div className="absolute bottom-10 left-1/2 -translate-x-1/2" animate={{ y: [0, 10, 0] }} transition={{ duration: 2, repeat: Infinity }}>
        <div className="w-6 h-10 rounded-full border-2 border-[var(--color-text-muted)] flex items-start justify-center p-1">
          <motion.div className="w-1.5 h-3 rounded-full bg-[var(--color-text-muted)]" animate={{ y: [0, 12, 0] }} transition={{ duration: 2, repeat: Infinity }} />
        </div>
      </motion.div>
    </section>
  );
}

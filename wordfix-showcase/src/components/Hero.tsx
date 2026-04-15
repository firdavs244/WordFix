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
    <section className="relative min-h-[calc(100vh-56px)] flex flex-col items-center justify-center px-6 py-20 overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <motion.div
          className="absolute w-72 h-72 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(59,130,246,0.12), transparent)', top: '10%', left: '10%' }}
          animate={{ y: [0, -30, 0], x: [0, 15, 0] }}
          transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute w-96 h-96 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(139,92,246,0.1), transparent)', bottom: '10%', right: '10%' }}
          animate={{ y: [0, 20, 0], x: [0, -20, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute w-48 h-48 rounded-full"
          style={{ background: 'radial-gradient(circle, rgba(16,185,129,0.1), transparent)', top: '50%', right: '30%' }}
          animate={{ y: [0, -25, 0] }}
          transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
        />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 text-center max-w-3xl mx-auto w-full"
      >
        <motion.div
          className="inline-block mb-8 px-5 py-2 rounded-full border border-[var(--color-border-glass)] text-sm text-[var(--color-text-secondary)]"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          11 Pod &bull; 5 HPA &bull; 7 PDB &bull; Zero-Trust Network &bull; k3s Klaster
        </motion.div>

        <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold mb-6 leading-[1.1]">
          <span className="text-[var(--color-text-primary)]">WordFix</span>
          <br />
          <span className="gradient-text inline-block min-h-[1.2em]">
            <motion.span
              key={wordIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="inline-block"
            >
              {words[wordIndex]}
            </motion.span>
          </span>
        </h1>

        <motion.p
          className="text-base md:text-lg text-[var(--color-text-secondary)] max-w-xl mx-auto mb-10 leading-relaxed"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          Production-darajadagi til o'rganish platformasi. Mikroservis arxitektura,
          Kubernetes infratuzilma, DDD dizayn va so'rov oqimini quyida batafsil ko'ring.
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
        >
          <motion.a
            href="#architecture"
            className="btn btn-primary px-8 py-3 rounded-full text-base"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
          >
            Arxitekturani Ko'rish
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
          </motion.a>
          <motion.a
            href="#ddd"
            className="btn px-8 py-3 rounded-full text-base border border-[var(--color-border-glass)] text-[var(--color-text-secondary)] hover:text-white hover:border-[var(--color-accent-purple)]"
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.97 }}
          >
            DDD Strukturasi
          </motion.a>
        </motion.div>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
        animate={{ y: [0, 8, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="w-5 h-8 rounded-full border-2 border-[var(--color-text-muted)] flex items-start justify-center pt-1">
          <motion.div
            className="w-1 h-2 rounded-full bg-[var(--color-text-muted)]"
            animate={{ y: [0, 10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </div>
      </motion.div>
    </section>
  );
}

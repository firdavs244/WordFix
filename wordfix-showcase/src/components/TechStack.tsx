import { motion } from 'framer-motion';
import { techStack } from '../data/architecture';
import {
  Code2, FileCode2, Zap, Palette, Move, Server, Rocket, Clock,
  Database, HardDrive, MessageSquare, Container, Globe, Box, Brain, Sparkles
} from 'lucide-react';

const iconMap: Record<string, React.ComponentType<{ size?: number; className?: string; style?: React.CSSProperties }>> = {
  Code2, FileCode2, Zap, Palette, Move, Server, Rocket, Clock,
  Database, HardDrive, MessageSquare, Container, Globe, Box, Brain, Sparkles,
};

const categoryColors: Record<string, string> = {
  Frontend: 'var(--color-accent-blue)',
  Backend: 'var(--color-accent-purple)',
  Database: 'var(--color-accent-emerald)',
  Infra: 'var(--color-accent-amber)',
  AI: 'var(--color-accent-pink)',
};

export default function TechStack() {
  return (
    <section id="tech-stack" className="py-24 px-6 bg-[var(--color-bg-secondary)]">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-4">
          <span className="gradient-text">Tech Stack</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-12 max-w-2xl mx-auto">
          Modern technologies chosen for scalability, developer experience, and production readiness.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {techStack.map((tech, i) => {
            const Icon = iconMap[tech.icon];
            const color = categoryColors[tech.category];
            return (
              <motion.div
                key={tech.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                whileHover={{ scale: 1.05, y: -4 }}
                className="glass-card p-4 flex flex-col items-center gap-3 cursor-default"
              >
                {Icon && <Icon size={28} className="opacity-80" style={{ color }} />}
                <span className="text-sm font-semibold text-[var(--color-text-primary)]">{tech.name}</span>
                <span className="text-xs px-2 py-0.5 rounded-full" style={{ background: `${color}20`, color }}>{tech.category}</span>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </section>
  );
}

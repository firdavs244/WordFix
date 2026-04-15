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

const categoryBadge: Record<string, string> = {
  Frontend: 'badge-blue',
  Backend: 'badge-purple',
  "Ma'lumotlar bazasi": 'badge-emerald',
  Infratuzilma: 'badge-amber',
  "Sun'iy intellekt": 'badge-pink',
};

const categoryColor: Record<string, string> = {
  Frontend: '#3b82f6',
  Backend: '#8b5cf6',
  "Ma'lumotlar bazasi": '#10b981',
  Infratuzilma: '#f59e0b',
  "Sun'iy intellekt": '#ec4899',
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
          <span className="gradient-text">Texnologiya Steki</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-12 max-w-2xl mx-auto text-base leading-relaxed">
          Kengayuvchanlik, dasturchi tajribasi va ishlab chiqarishga tayyorlik uchun tanlangan zamonaviy texnologiyalar.
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {techStack.map((tech, i) => {
            const Icon = iconMap[tech.icon];
            const color = categoryColor[tech.category] || '#3b82f6';
            const badge = categoryBadge[tech.category] || 'badge-blue';
            return (
              <motion.div
                key={tech.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.04 }}
                whileHover={{ scale: 1.04, y: -3 }}
                className="glass-card-compact flex flex-col items-center gap-3 cursor-default text-center"
              >
                {Icon && <Icon size={26} style={{ color }} />}
                <span className="text-sm font-semibold text-[var(--color-text-primary)]">{tech.name}</span>
                <span className={`text-[11px] px-2 py-0.5 rounded-full font-medium ${badge}`}>
                  {tech.category}
                </span>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
    </section>
  );
}

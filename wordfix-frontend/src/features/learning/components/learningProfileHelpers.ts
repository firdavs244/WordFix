import { Eye, Headphones, BookOpen, Zap } from 'lucide-react';

// ─── Constants ─────────────────────────────────────────────────────────────────

export const styleConfig: Record<string, { icon: typeof Eye; label: string; color: string }> = {
  visual: { icon: Eye, label: 'Visual Learner', color: 'text-blue-500' },
  auditory: { icon: Headphones, label: 'Auditory Learner', color: 'text-purple-500' },
  reading: { icon: BookOpen, label: 'Reading/Writing Learner', color: 'text-green-500' },
  kinesthetic: { icon: Zap, label: 'Kinesthetic Learner', color: 'text-orange-500' },
};

export const styleBarColors: Record<string, string> = {
  visual: 'bg-blue-500',
  auditory: 'bg-purple-500',
  reading: 'bg-green-500',
  kinesthetic: 'bg-orange-500',
};

export const dayLabels = ['Du', 'Se', 'Cho', 'Pa', 'Ju', 'Sha', 'Ya'];

export const skillLabels: Record<string, string> = {
  reading: 'Reading',
  vocabulary: 'Vocabulary',
  listening: 'Listening',
  context: 'Context',
  speed: 'Speed',
};

export const reasonConfig: Record<string, { color: string; bgColor: string; label: string }> = {
  domain_gap: { color: 'text-green-700 dark:text-green-300', bgColor: 'bg-green-100 dark:bg-green-900', label: "Soha bo'yicha" },
  confusion_fix: { color: 'text-yellow-700 dark:text-yellow-300', bgColor: 'bg-yellow-100 dark:bg-yellow-900', label: 'Chalkashlik tuzatish' },
  level_appropriate: { color: 'text-blue-700 dark:text-blue-300', bgColor: 'bg-blue-100 dark:bg-blue-900', label: "Darajangizga mos" },
  high_frequency: { color: 'text-violet-700 dark:text-violet-300', bgColor: 'bg-violet-100 dark:bg-violet-900', label: "Ko'p ishlatiladigan" },
};

export const patternConfig: Record<string, { color: string; bgColor: string; label: string }> = {
  l1_interference: { color: 'text-red-700 dark:text-red-300', bgColor: 'bg-red-100 dark:bg-red-900', label: "Ona tili ta'siri" },
  morphological: { color: 'text-orange-700 dark:text-orange-300', bgColor: 'bg-orange-100 dark:bg-orange-900', label: "So'z shakli" },
  semantic: { color: 'text-yellow-700 dark:text-yellow-300', bgColor: 'bg-yellow-100 dark:bg-yellow-900', label: "Ma'no almashish" },
  spelling: { color: 'text-blue-700 dark:text-blue-300', bgColor: 'bg-blue-100 dark:bg-blue-900', label: 'Imlo' },
  phonological: { color: 'text-violet-700 dark:text-violet-300', bgColor: 'bg-violet-100 dark:bg-violet-900', label: 'Talaffuz' },
};

// ─── Animation Variants ────────────────────────────────────────────────────────

export const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

export const sectionVariants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: 'easeOut' as const } },
};

// ─── Helpers ───────────────────────────────────────────────────────────────────

export function formatTimeAgo(dateStr: string | null): string {
  if (!dateStr) return '';
  const diff = Date.now() - new Date(dateStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 60) return `${minutes} daqiqa oldin`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} soat oldin`;
  const days = Math.floor(hours / 24);
  return `${days} kun oldin`;
}

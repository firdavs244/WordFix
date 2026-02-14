import {
  BookOpen,
  Search,
  Sword,
  Laugh,
  Rocket,
  Home,
  Plane,
  Wand2,
  Ghost,
} from 'lucide-react';

// ─── Types ─────────────────────────────────────────────────────────────────────

export type Phase = 'GENRE_SELECT' | 'PLAYING' | 'COMPLETE';

export interface StorySegment {
  type: 'ai' | 'user';
  text: string;
  roundNumber: number;
}

// ─── Genre Data ────────────────────────────────────────────────────────────────

export const GENRES = [
  { key: 'adventure', label: 'Adventure', icon: Sword, emoji: '🗡️' },
  { key: 'mystery', label: 'Mystery', icon: Search, emoji: '🔍' },
  { key: 'comedy', label: 'Comedy', icon: Laugh, emoji: '😂' },
  { key: 'sci-fi', label: 'Sci-Fi', icon: Rocket, emoji: '🚀' },
  { key: 'daily_life', label: 'Daily Life', icon: Home, emoji: '🏠' },
  { key: 'travel', label: 'Travel', icon: Plane, emoji: '✈️' },
  { key: 'fantasy', label: 'Fantasy', icon: Wand2, emoji: '🧙' },
  { key: 'thriller', label: 'Thriller', icon: Ghost, emoji: '👻' },
] as const;

// ─── Helpers ───────────────────────────────────────────────────────────────────

export function getStars(score: number, maxScore: number) {
  const pct = maxScore > 0 ? (score / maxScore) * 100 : 0;
  if (pct >= 90) return 5;
  if (pct >= 75) return 4;
  if (pct >= 60) return 3;
  if (pct >= 40) return 2;
  if (pct >= 20) return 1;
  return 0;
}

export function getRoundStars(score: number) {
  if (score >= 18) return 5;
  if (score >= 15) return 4;
  if (score >= 12) return 3;
  if (score >= 8) return 2;
  if (score >= 4) return 1;
  return 0;
}

export function fireConfetti() {
  import('canvas-confetti')
    .then((mod) => {
      const confetti = mod.default;
      confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
    })
    .catch(() => {});
}

export function formatTime(s: number) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${sec.toString().padStart(2, '0')}`;
}

export { BookOpen };

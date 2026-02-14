import { useState, useEffect, useRef, useCallback } from 'react';

// ─── Types ─────────────────────────────────────────────────────────────────────

export type ListeningPhase = 'READY' | 'PLAYING' | 'COMPLETE';
export type FeedbackType = 'correct' | 'wrong' | 'failed' | null;

export interface RoundState {
  roundNumber: number;
  audioUrl: string;
  hint: string;
  maxAttempts: number;
  attemptsUsed: number;
}

// ─── Audio Hook ────────────────────────────────────────────────────────────────

export function useAudioPlayer(url: string) {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!url) return;
    const audio = new Audio(url);
    audioRef.current = audio;
    audio.addEventListener('ended', () => setIsPlaying(false));
    audio.addEventListener('error', () => setIsPlaying(false));
    return () => {
      audio.pause();
      audio.removeEventListener('ended', () => setIsPlaying(false));
      audio.removeEventListener('error', () => setIsPlaying(false));
    };
  }, [url]);

  const play = useCallback(() => {
    if (!audioRef.current || !url) return;
    audioRef.current.currentTime = 0;
    audioRef.current
      .play()
      .then(() => setIsPlaying(true))
      .catch(() => {});
  }, [url]);

  return { play, isPlaying };
}

// ─── Helpers ───────────────────────────────────────────────────────────────────

export function getStars(pct: number) {
  if (pct >= 90) return 5;
  if (pct >= 75) return 4;
  if (pct >= 60) return 3;
  if (pct >= 40) return 2;
  if (pct >= 20) return 1;
  return 0;
}

export function getAttemptLabel(attempts: number) {
  switch (attempts) {
    case 1:
      return '1st try';
    case 2:
      return '2nd try';
    case 3:
      return '3rd try';
    default:
      return `${attempts}th try`;
  }
}

export function fireConfetti() {
  import('canvas-confetti')
    .then((mod) => {
      const confetti = mod.default;
      confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
    })
    .catch(() => {});
}

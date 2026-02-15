import { useCallback } from 'react';
import confetti from 'canvas-confetti';

interface ConfettiOptions {
  particleCount?: number;
  spread?: number;
  origin?: { x?: number; y?: number };
  colors?: string[];
}

export function useConfetti() {
  const fireConfetti = useCallback((options?: ConfettiOptions) => {
    confetti({
      particleCount: options?.particleCount ?? 100,
      spread: options?.spread ?? 70,
      origin: { y: 0.6, ...options?.origin },
      colors: options?.colors,
    });
  }, []);

  return { fireConfetti };
}

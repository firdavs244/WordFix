import { create } from 'zustand';
import type { ReviewQuality, ReviewSession, Word } from '@/types';

interface ReviewState {
  // Session state
  currentSession: ReviewSession | null;
  words: Word[];
  currentIndex: number;
  isFlipped: boolean;
  answers: Map<string, ReviewQuality>;

  // Actions
  setSession: (session: ReviewSession) => void;
  setWords: (words: Word[]) => void;
  flipCard: () => void;
  setFlipped: (flipped: boolean) => void;
  recordAnswer: (wordId: string, quality: ReviewQuality) => void;
  nextWord: () => void;
  previousWord: () => void;
  reset: () => void;

  // Computed
  currentWord: () => Word | null;
  progress: () => number;
  isLastWord: () => boolean;
  totalAnswered: () => number;
}

export const useReviewStore = create<ReviewState>((set, get) => ({
  currentSession: null,
  words: [],
  currentIndex: 0,
  isFlipped: false,
  answers: new Map(),

  setSession: (session) => set({ currentSession: session }),

  setWords: (words) => set({ words, currentIndex: 0, isFlipped: false, answers: new Map() }),

  flipCard: () => set((state) => ({ isFlipped: !state.isFlipped })),

  setFlipped: (flipped) => set({ isFlipped: flipped }),

  recordAnswer: (wordId, quality) =>
    set((state) => {
      const newAnswers = new Map(state.answers);
      newAnswers.set(wordId, quality);
      return { answers: newAnswers };
    }),

  nextWord: () =>
    set((state) => ({
      currentIndex: Math.min(state.currentIndex + 1, state.words.length - 1),
      isFlipped: false,
    })),

  previousWord: () =>
    set((state) => ({
      currentIndex: Math.max(state.currentIndex - 1, 0),
      isFlipped: false,
    })),

  reset: () =>
    set({
      currentSession: null,
      words: [],
      currentIndex: 0,
      isFlipped: false,
      answers: new Map(),
    }),

  currentWord: () => {
    const { words, currentIndex } = get();
    return words[currentIndex] ?? null;
  },

  progress: () => {
    const { words, answers } = get();
    if (words.length === 0) return 0;
    return (answers.size / words.length) * 100;
  },

  isLastWord: () => {
    const { words, currentIndex } = get();
    return currentIndex >= words.length - 1;
  },

  totalAnswered: () => get().answers.size,
}));

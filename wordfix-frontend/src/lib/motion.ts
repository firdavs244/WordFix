export const pageTransition = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.3, ease: [0.25, 0.46, 0.45, 0.94] as const } },
  exit: { opacity: 0, y: -8, transition: { duration: 0.15 } },
} as const;

export const staggerContainer = {
  animate: { transition: { staggerChildren: 0.04, delayChildren: 0.06 } },
};

export const staggerItem = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.25, ease: 'easeOut' as const } },
} as const;

export const fadeInUp = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.25, 0.46, 0.45, 0.94] as const } },
} as const;

export const fadeIn = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
};

export const scaleIn = {
  initial: { opacity: 0, scale: 0.95 },
  animate: { opacity: 1, scale: 1, transition: { duration: 0.2, ease: [0.25, 0.46, 0.45, 0.94] as const } },
  exit: { opacity: 0, scale: 0.95, transition: { duration: 0.15 } },
} as const;

export const cardHover = {
  rest: { y: 0, boxShadow: 'var(--shadow-card)' },
  hover: { y: -3, boxShadow: 'var(--shadow-card-hover)', transition: { type: 'spring', stiffness: 400, damping: 25 } } as const,
  tap: { scale: 0.98, transition: { duration: 0.1 } },
};

export const slideInRight = {
  initial: { opacity: 0, x: 16 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.25, ease: 'easeOut' as const } },
  exit: { opacity: 0, x: 16, transition: { duration: 0.15 } },
} as const;

export const slideInLeft = {
  initial: { opacity: 0, x: -16 },
  animate: { opacity: 1, x: 0, transition: { duration: 0.25, ease: 'easeOut' as const } },
  exit: { opacity: 0, x: -16, transition: { duration: 0.15 } },
} as const;

export const counterSpring = { type: 'spring' as const, stiffness: 100, damping: 15 };

export const progressFill = (percentage: number, delay = 0.2) => ({
  initial: { width: 0 },
  animate: { width: `${percentage}%`, transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] as const, delay } },
});

export const bounceIn = {
  initial: { opacity: 0, scale: 0.3 },
  animate: { opacity: 1, scale: 1, transition: { type: 'spring' as const, stiffness: 200, damping: 12 } },
};

export const shake = {
  animate: { x: [0, -8, 8, -6, 6, -3, 3, 0], transition: { duration: 0.4 } },
};

export const floatUp = {
  initial: { opacity: 0, y: 10, scale: 0.8 },
  animate: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, y: -20, transition: { duration: 0.5 } },
};

export const flipCard = {
  front: (isFlipped: boolean) => ({
    rotateY: isFlipped ? 180 : 0,
    transition: { type: 'spring', stiffness: 300, damping: 30 },
  }),
  back: (isFlipped: boolean) => ({
    rotateY: isFlipped ? 0 : -180,
    transition: { type: 'spring', stiffness: 300, damping: 30 },
  }),
};

import { useEffect, useRef } from 'react';
import { useMotionValue, useSpring, useTransform, motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AnimatedCounterProps {
  value: number;
  duration?: number;
  className?: string;
  prefix?: string;
  suffix?: string;
}

export default function AnimatedCounter({ value, duration = 0.8, className, prefix, suffix }: AnimatedCounterProps) {
  const motionValue = useMotionValue(0);
  const spring = useSpring(motionValue, { duration: duration * 1000 });
  const display = useTransform(spring, (v) => Math.round(v));
  const ref = useRef<HTMLSpanElement>(null);

  useEffect(() => { motionValue.set(value); }, [value, motionValue]);
  useEffect(() => {
    const unsubscribe = display.on('change', (v) => {
      if (ref.current) ref.current.textContent = `${prefix ?? ''}${v}${suffix ?? ''}`;
    });
    return unsubscribe;
  }, [display, prefix, suffix]);

  return <motion.span ref={ref} className={cn(className)} />;
}

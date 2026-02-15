import { useMemo } from 'react';
import { motion } from 'framer-motion';
import { fadeInUp } from '@/lib/motion';
import { GradientText } from '@/components/shared';
import { useAuthStore } from '@/stores/useAuthStore';

const QUOTES = [
  'Every word brings you closer to fluency',
  'Small steps, big vocabulary',
  'Consistency beats intensity',
  'Your brain is a word machine',
  'Today is a great day to learn',
];

function getGreeting(hour: number): { text: string; emoji: string } {
  if (hour >= 5 && hour < 12) return { text: 'Good morning', emoji: '☀️' };
  if (hour >= 12 && hour < 18) return { text: 'Good afternoon', emoji: '🌤️' };
  if (hour >= 18) return { text: 'Good evening', emoji: '🌙' };
  return { text: 'Burning the midnight oil', emoji: '🌟' };
}

export default function WelcomeHeader() {
  const user = useAuthStore((s) => s.user);
  const firstName = user?.full_name?.split(' ')[0] || user?.username || 'Learner';

  const { greeting, quote, dateStr } = useMemo(() => {
    const now = new Date();
    const g = getGreeting(now.getHours());
    return {
      greeting: g,
      quote: QUOTES[Math.floor(Math.random() * QUOTES.length)],
      dateStr: now.toLocaleDateString('en-US', {
        weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
      }),
    };
  }, []);

  return (
    <motion.div
      variants={fadeInUp}
      initial="initial"
      animate="animate"
      className="relative overflow-hidden rounded-2xl p-6 lg:p-8"
      style={{
        background: [
          'radial-gradient(ellipse at 20% 50%, hsl(var(--primary) / 0.04) 0%, transparent 50%)',
          'radial-gradient(ellipse at 80% 50%, hsl(var(--secondary) / 0.03) 0%, transparent 50%)',
          'radial-gradient(ellipse at 50% 100%, hsl(var(--accent) / 0.02) 0%, transparent 50%)',
        ].join(', '),
      }}
    >
      {/* Noise overlay */}
      <div className="pointer-events-none absolute inset-0 opacity-[0.02]" style={{
        backgroundImage: "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")",
      }} />

      <div className="relative z-10 flex items-center justify-between">
        <div className="flex-1">
          <h1 className="text-2xl lg:text-3xl font-heading font-bold tracking-tight">
            {greeting.text}, <GradientText>{firstName}</GradientText>! {greeting.emoji}
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">{dateStr}</p>
          <p className="mt-0.5 text-sm text-muted-foreground/60 italic">{quote}</p>
        </div>

        {/* Decorative floating word card */}
        <div className="hidden lg:block">
          <div className="rotate-3 animate-float rounded-xl border border-border/30 bg-card/80 px-5 py-3 shadow-lg backdrop-blur-sm opacity-60">
            <p className="text-xs text-muted-foreground">Word of the day</p>
            <p className="font-heading font-semibold text-sm mt-0.5">Serendipity</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

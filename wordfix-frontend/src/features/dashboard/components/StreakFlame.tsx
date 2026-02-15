import { Flame } from 'lucide-react';

interface StreakFlameProps {
  active: boolean;
  size?: number;
}

export default function StreakFlame({ active, size = 28 }: StreakFlameProps) {
  if (!active) {
    return (
      <div className="flex h-[52px] w-[52px] items-center justify-center rounded-2xl bg-muted/30">
        <Flame className="h-7 w-7 text-muted-foreground/30" />
      </div>
    );
  }

  return (
    <div className="relative flex h-[52px] w-[52px] items-center justify-center rounded-2xl bg-gradient-to-br from-orange-500/10 to-amber-500/10">
      {/* Glow layer */}
      <Flame
        className="absolute text-orange-400 blur-[8px] opacity-40"
        style={{ width: size + 6, height: size + 6 }}
      />
      {/* Main flame */}
      <Flame
        className="relative text-orange-500 animate-[flicker_1.5s_ease-in-out_infinite]"
        style={{ width: size, height: size }}
      />
      {/* Particles floating upward */}
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="absolute h-[3px] w-[3px] rounded-full bg-orange-400/60 animate-[spark_2s_ease-out_infinite]"
          style={{
            left: `${40 + i * 10}%`,
            bottom: '65%',
            animationDelay: `${i * 0.5}s`,
          }}
        />
      ))}
    </div>
  );
}

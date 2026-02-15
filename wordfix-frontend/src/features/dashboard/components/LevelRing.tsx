import { motion } from 'framer-motion';

interface LevelRingProps {
  level: number;
  progress: number;
  size?: number;
}

export default function LevelRing({ level, progress, size = 88 }: LevelRingProps) {
  const strokeW = 5;
  const radius = (size - strokeW) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (Math.min(progress, 100) / 100) * circumference;
  const center = size / 2;

  return (
    <svg width={size} height={size} className="-rotate-90">
      <defs>
        <linearGradient id="lvl-grad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="hsl(var(--primary))" />
          <stop offset="100%" stopColor="hsl(var(--secondary))" />
        </linearGradient>
      </defs>
      <circle
        cx={center} cy={center} r={radius}
        fill="none" stroke="hsl(var(--muted))" strokeWidth={strokeW}
      />
      <motion.circle
        cx={center} cy={center} r={radius}
        fill="none" stroke="url(#lvl-grad)"
        strokeWidth={strokeW} strokeLinecap="round"
        strokeDasharray={circumference}
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset: offset }}
        transition={{ duration: 1.2, ease: [0.25, 0.46, 0.45, 0.94], delay: 0.3 }}
      />
      <g transform={`rotate(90 ${center} ${center})`}>
        <text
          x={center} y={center - 4}
          textAnchor="middle" dominantBaseline="central"
          className="fill-foreground font-heading text-xl font-bold"
          style={{ fontSize: size * 0.28 }}
        >
          {level}
        </text>
        <text
          x={center} y={center + size * 0.16}
          textAnchor="middle" dominantBaseline="central"
          className="fill-muted-foreground font-heading font-semibold uppercase"
          style={{ fontSize: size * 0.11 }}
        >
          LVL
        </text>
      </g>
    </svg>
  );
}

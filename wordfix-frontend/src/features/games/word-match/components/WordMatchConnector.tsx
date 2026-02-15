interface MatchedPair {
  wordPos: { x: number; y: number };
  translationPos: { x: number; y: number };
}

interface Props {
  pairs: MatchedPair[];
}

export default function WordMatchConnector({ pairs }: Props) {
  if (!pairs.length) return null;

  return (
    <svg className="pointer-events-none absolute inset-0 z-10 h-full w-full">
      {pairs.map((p, i) => (
        <line
          key={i}
          x1={p.wordPos.x}
          y1={p.wordPos.y}
          x2={p.translationPos.x}
          y2={p.translationPos.y}
          stroke="hsl(var(--success))"
          strokeWidth="2"
          strokeDasharray="4 4"
          opacity="0.4"
        />
      ))}
    </svg>
  );
}

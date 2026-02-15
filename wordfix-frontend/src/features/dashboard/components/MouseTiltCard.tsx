import { useState, useCallback, type ReactNode, type MouseEvent } from 'react';
import { cn } from '@/lib/utils';

interface MouseTiltCardProps {
  children: ReactNode;
  className?: string;
  tiltAmount?: number;
  glare?: boolean;
  scale?: number;
}

export default function MouseTiltCard({
  children,
  className,
  tiltAmount = 4,
  glare = false,
  scale = 1.02,
}: MouseTiltCardProps) {
  const [tilt, setTilt] = useState({ rx: 0, ry: 0, mx: 50, my: 50 });
  const [hovered, setHovered] = useState(false);

  const handleMove = useCallback(
    (e: MouseEvent<HTMLDivElement>) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const mx = ((e.clientX - rect.left) / rect.width) * 100;
      const my = ((e.clientY - rect.top) / rect.height) * 100;
      const rx = ((my - 50) / 50) * tiltAmount;
      const ry = ((mx - 50) / 50) * -tiltAmount;
      setTilt({ rx, ry, mx, my });
    },
    [tiltAmount],
  );

  const handleLeave = useCallback(() => {
    setHovered(false);
    setTilt({ rx: 0, ry: 0, mx: 50, my: 50 });
  }, []);

  return (
    <div
      className={cn('relative', className)}
      style={{
        transformStyle: 'preserve-3d',
        transform: `perspective(800px) rotateX(${tilt.rx}deg) rotateY(${tilt.ry}deg) scale(${hovered ? scale : 1})`,
        transition: hovered ? 'transform 0.15s ease-out' : 'transform 0.5s cubic-bezier(0.25,0.46,0.45,0.94)',
      }}
      onMouseMove={handleMove}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={handleLeave}
    >
      {children}
      {glare && hovered && (
        <div
          className="pointer-events-none absolute inset-0 z-10 rounded-2xl opacity-100 transition-opacity"
          style={{
            background: `radial-gradient(circle at ${tilt.mx}% ${tilt.my}%, rgba(255,255,255,0.08) 0%, transparent 60%)`,
          }}
        />
      )}
    </div>
  );
}

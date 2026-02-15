import { cn } from '@/lib/utils';

interface Props {
  isPlaying: boolean;
}

export default function AudioWaveform({ isPlaying }: Props) {
  const bars = Array.from({ length: 24 }, (_, i) => i);

  return (
    <div className="flex h-12 items-center justify-center gap-0.5" data-testid="audio-waveform">
      {bars.map((i) => (
        <div
          key={i}
          className={cn(
            'w-0.5 rounded-full bg-primary/60 transition-all',
            isPlaying ? 'animate-waveform' : 'h-1',
          )}
          style={isPlaying ? {
            animationDelay: `${i * 0.05}s`,
            animationDuration: `${0.4 + Math.random() * 0.4}s`,
          } : { height: '4px' }}
        />
      ))}
      <style>{`
        @keyframes waveform {
          0%, 100% { height: 4px; }
          50% { height: ${Math.random() * 24 + 16}px; }
        }
        .animate-waveform { animation: waveform 0.6s ease-in-out infinite alternate; }
      `}</style>
    </div>
  );
}

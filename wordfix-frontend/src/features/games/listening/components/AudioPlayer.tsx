import { useState } from 'react';
import { Play, Pause, RotateCcw } from 'lucide-react';
import AudioWaveform from './AudioWaveform';

interface Props {
  audioUrl: string;
  onPlay?: () => void;
}

export default function AudioPlayer({ audioUrl: _audioUrl, onPlay }: Props) {
  const [isPlaying, setIsPlaying] = useState(false);

  const handleToggle = () => {
    setIsPlaying((p) => !p);
    onPlay?.();
  };

  const handleReplay = () => {
    setIsPlaying(true);
    onPlay?.();
  };

  return (
    <div className="flex flex-col items-center" data-testid="audio-player">
      <button
        type="button"
        onClick={handleToggle}
        className="flex h-[72px] w-[72px] items-center justify-center rounded-full bg-gradient-to-br from-primary to-primary/80 text-white shadow-lg transition-transform hover:scale-105 active:scale-95"
        aria-label={isPlaying ? 'Pause' : 'Play'}
        data-testid="play-button"
      >
        {isPlaying ? <Pause className="h-8 w-8" /> : <Play className="ml-1 h-8 w-8" />}
      </button>

      <div className="mt-4">
        <AudioWaveform isPlaying={isPlaying} />
      </div>

      <button
        type="button"
        onClick={handleReplay}
        className="mt-3 flex items-center gap-1.5 rounded-lg border border-border/50 px-3 py-1.5 text-xs text-muted-foreground transition-colors hover:bg-muted/30"
        data-testid="replay-button"
      >
        <RotateCcw className="h-3 w-3" /> Replay
      </button>
    </div>
  );
}

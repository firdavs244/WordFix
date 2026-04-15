import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Pause, Volume2 } from 'lucide-react';
import { fadeIn } from '@/lib/motion';
import useAudioPlayer from '../../hooks/useAudioPlayer';

interface AudioPlayerProps {
  audioUrl: string;
  autoPlay?: boolean;
}

function formatTime(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

export default function AudioPlayer({ audioUrl, autoPlay = false }: AudioPlayerProps) {
  const { isPlaying, progress, duration, currentTime, isLoaded, load, toggle } = useAudioPlayer();

  useEffect(() => {
    if (audioUrl) {
      load(audioUrl);
    }
  }, [audioUrl, load]);

  useEffect(() => {
    if (autoPlay && isLoaded && !isPlaying) {
      toggle();
    }
    // Only auto-play once when loaded
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoaded]);

  if (!audioUrl) return null;

  return (
    <motion.div
      {...fadeIn}
      role="region"
      aria-label="NPC audio player"
      className="mt-1 flex items-center gap-2 rounded-lg bg-gray-100 px-3 py-1.5 dark:bg-gray-700/50"
    >
      <button
        onClick={toggle}
        disabled={!isLoaded}
        aria-label={isPlaying ? 'Pause audio' : 'Play audio'}
        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-500 text-white transition-colors hover:bg-indigo-600 disabled:opacity-40"
      >
        {isPlaying ? <Pause className="h-3.5 w-3.5" /> : <Play className="ml-0.5 h-3.5 w-3.5" />}
      </button>

      <div className="flex flex-1 items-center gap-2">
        <div className="relative h-1.5 flex-1 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-600">
          <motion.div
            className="absolute inset-y-0 left-0 rounded-full bg-indigo-500"
            style={{ width: `${progress}%` }}
            transition={{ duration: 0.1 }}
          />
        </div>
        <span className="min-w-[3.5rem] text-xs text-gray-500 dark:text-gray-400">
          {isLoaded ? `${formatTime(currentTime)} / ${formatTime(duration)}` : '...'}
        </span>
      </div>

      <Volume2 className="h-3.5 w-3.5 shrink-0 text-gray-400" aria-hidden="true" />
    </motion.div>
  );
}

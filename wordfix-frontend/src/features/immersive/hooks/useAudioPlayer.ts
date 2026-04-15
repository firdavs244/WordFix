import { useCallback, useEffect, useRef, useState } from 'react';

interface AudioPlayerState {
  isPlaying: boolean;
  progress: number;
  duration: number;
  currentTime: number;
  isLoaded: boolean;
}

export default function useAudioPlayer() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [state, setState] = useState<AudioPlayerState>({
    isPlaying: false,
    progress: 0,
    duration: 0,
    currentTime: 0,
    isLoaded: false,
  });

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current.src = '';
        audioRef.current = null;
      }
    };
  }, []);

  const load = useCallback((url: string) => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.src = '';
    }

    const audio = new Audio(url);
    audioRef.current = audio;

    audio.addEventListener('loadedmetadata', () => {
      setState((s) => ({ ...s, duration: audio.duration, isLoaded: true }));
    });

    audio.addEventListener('timeupdate', () => {
      const progress = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
      setState((s) => ({ ...s, currentTime: audio.currentTime, progress }));
    });

    audio.addEventListener('ended', () => {
      setState((s) => ({ ...s, isPlaying: false, progress: 100 }));
    });

    audio.addEventListener('error', () => {
      setState((s) => ({ ...s, isPlaying: false, isLoaded: false }));
    });
  }, []);

  const play = useCallback(async () => {
    if (audioRef.current) {
      await audioRef.current.play();
      setState((s) => ({ ...s, isPlaying: true }));
    }
  }, []);

  const pause = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      setState((s) => ({ ...s, isPlaying: false }));
    }
  }, []);

  const toggle = useCallback(async () => {
    if (state.isPlaying) {
      pause();
    } else {
      await play();
    }
  }, [state.isPlaying, play, pause]);

  const seek = useCallback((time: number) => {
    if (audioRef.current) {
      audioRef.current.currentTime = time;
    }
  }, []);

  const reset = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setState((s) => ({ ...s, isPlaying: false, progress: 0, currentTime: 0 }));
    }
  }, []);

  return { ...state, load, play, pause, toggle, seek, reset };
}

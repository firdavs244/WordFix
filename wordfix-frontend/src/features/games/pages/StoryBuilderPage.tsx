import { useState, useEffect, useRef, useCallback } from 'react';
import { Loader2 } from 'lucide-react';
import { PageTransition } from '@/components/animations/PageTransition';
import {
  useStartStoryBuilder,
  useSubmitStoryRound,
  useCompleteStoryBuilder,
} from '../hooks/useGames';
import { toast } from 'sonner';
import type {
  StoryStartResponse,
  StorySubmitResponse,
  StoryCompleteResponse,
  StoryRoundResult,
} from '@/types';
import { fireConfetti, type Phase, type StorySegment } from '../components/storyBuilderHelpers';
import { GenreSelect } from '../components/GenreSelect';
import { StoryPlaying } from '../components/StoryPlaying';
import { StoryComplete } from '../components/StoryComplete';

// ─── Main Component ────────────────────────────────────────────────────────────

export function StoryBuilderPage() {
  const startMutation = useStartStoryBuilder();
  const submitMutation = useSubmitStoryRound();
  const completeMutation = useCompleteStoryBuilder();

  // Phase
  const [phase, setPhase] = useState<Phase>('GENRE_SELECT');

  // Genre
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  // Session
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [totalRounds, setTotalRounds] = useState(5);
  const [currentRound, setCurrentRound] = useState(1);
  const [targetWords, setTargetWords] = useState<string[]>([]);
  const [allTargetWords, setAllTargetWords] = useState<string[]>([]);

  // Story segments
  const [segments, setSegments] = useState<StorySegment[]>([]);

  // User input
  const [userText, setUserText] = useState('');

  // Timer
  const [timeElapsed, setTimeElapsed] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Round result
  const [showResult, setShowResult] = useState(false);
  const [roundResult, setRoundResult] = useState<StoryRoundResult | null>(null);
  const [roundXp, setRoundXp] = useState(0);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState(0);

  // Combo
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);

  // Complete
  const [completeData, setCompleteData] = useState<StoryCompleteResponse | null>(null);

  // Timer
  useEffect(() => {
    if (phase === 'PLAYING' && !showResult) {
      timerRef.current = setInterval(() => {
        setTimeElapsed((t) => t + 1);
      }, 1000);
      return () => {
        if (timerRef.current) clearInterval(timerRef.current);
      };
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [phase, showResult]);

  // Auto-advance countdown
  useEffect(() => {
    if (!showResult || autoAdvanceTimer <= 0) return;
    const t = setInterval(() => {
      setAutoAdvanceTimer((v) => {
        if (v <= 1) {
          clearInterval(t);
          handleNextRound();
          return 0;
        }
        return v - 1;
      });
    }, 1000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [showResult, autoAdvanceTimer > 0]);

  // ─── Start Game ────────────────────────────────────────────────────────────

  const handleStart = () => {
    if (!selectedGenre) return;
    startMutation.mutate(selectedGenre, {
      onSuccess: (res) => {
        const d = res.data as StoryStartResponse;
        setSessionId(d.session_id);
        setTotalRounds(d.total_rounds);
        setCurrentRound(d.current_round);
        setTargetWords(d.target_words);
        setAllTargetWords(d.all_target_words);
        setSegments([{ type: 'ai', text: d.ai_text, roundNumber: 1 }]);
        setPhase('PLAYING');
      },
    });
  };

  // ─── Submit Round ──────────────────────────────────────────────────────────

  const handleSubmit = () => {
    if (!sessionId || userText.trim().length < 10 || submitMutation.isPending) return;
    submitMutation.mutate(
      { sessionId, userText: userText.trim() },
      {
        onSuccess: (res) => {
          const d = res.data as StorySubmitResponse;
          setSegments((prev) => [
            ...prev,
            { type: 'user', text: userText.trim(), roundNumber: currentRound },
          ]);
          setUserText('');
          setRoundResult(d.round_result);
          setRoundXp(d.xp_earned);
          setCombo(d.combo);
          setMultiplier(d.multiplier);
          setShowResult(true);
          setAutoAdvanceTimer(5);
        },
        onError: () => {
          toast.error('Failed to submit your text. Try again.');
        },
      },
    );
  };

  // ─── Next Round / Complete ─────────────────────────────────────────────────

  const handleNextRound = useCallback(() => {
    setShowResult(false);
    setAutoAdvanceTimer(0);

    if (submitMutation.data) {
      const d = submitMutation.data.data as StorySubmitResponse;
      if (d.next_round) {
        setSegments((prev) => [
          ...prev,
          { type: 'ai', text: d.next_round!.ai_text, roundNumber: d.next_round!.round_number },
        ]);
        setCurrentRound(d.next_round!.round_number);
        setTargetWords(d.next_round!.target_words);
      } else {
        handleComplete();
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [submitMutation.data]);

  const handleComplete = () => {
    if (!sessionId) return;
    completeMutation.mutate(sessionId, {
      onSuccess: (res) => {
        const d = res.data as StoryCompleteResponse;
        setCompleteData(d);
        setPhase('COMPLETE');
        if (d.max_score > 0 && (d.total_score / d.max_score) * 100 >= 80) {
          fireConfetti();
        }
      },
    });
  };

  const handlePlayAgain = () => {
    setPhase('GENRE_SELECT');
    setSessionId(null);
    setSegments([]);
    setCompleteData(null);
    setTimeElapsed(0);
    setCombo(0);
    setMultiplier(1);
    setCurrentRound(1);
  };

  // ─── RENDER ────────────────────────────────────────────────────────────────

  if (phase === 'GENRE_SELECT') {
    return (
      <GenreSelect
        selectedGenre={selectedGenre}
        onSelectGenre={setSelectedGenre}
        onStart={handleStart}
        isPending={startMutation.isPending}
      />
    );
  }

  if (phase === 'PLAYING') {
    return (
      <StoryPlaying
        currentRound={currentRound}
        totalRounds={totalRounds}
        targetWords={targetWords}
        allTargetWords={allTargetWords}
        segments={segments}
        userText={userText}
        onUserTextChange={setUserText}
        onSubmit={handleSubmit}
        isSubmitting={submitMutation.isPending}
        timeElapsed={timeElapsed}
        showResult={showResult}
        roundResult={roundResult}
        roundXp={roundXp}
        combo={combo}
        multiplier={multiplier}
        autoAdvanceTimer={autoAdvanceTimer}
        onNextRound={handleNextRound}
      />
    );
  }

  if (phase === 'COMPLETE' && completeData) {
    return <StoryComplete completeData={completeData} onPlayAgain={handlePlayAgain} />;
  }

  return (
    <PageTransition>
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    </PageTransition>
  );
}

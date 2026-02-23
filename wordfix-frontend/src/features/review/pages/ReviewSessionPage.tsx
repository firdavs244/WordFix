import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { FlashCard, QualityRating, ComboIndicator, ComboBreakEffect } from '../components';
import { XPGainPopup } from '@/components/common/XPGainPopup';
import { useReviewStore } from '@/stores/useReviewStore';
import { useSubmitAnswer, useCompleteSession, useReviewWords } from '../hooks/useReview';
import type { ReviewQuality, Word } from '@/types';

export function ReviewSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const [showRating, setShowRating] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);
  const [showComboBreak, setShowComboBreak] = useState(false);
  const [xpPopup, setXpPopup] = useState<{ xp: number; multiplier: number } | null>(null);
  const flipTimeRef = useRef<number>(0);

  const {
    words,
    currentIndex,
    isFlipped,
    answers,
    setSession,
    setWords,
    flipCard,
    setFlipped,
    recordAnswer,
    nextWord,
    reset,
  } = useReviewStore();

  const submitAnswer = useSubmitAnswer(sessionId!);
  const completeSession = useCompleteSession();
  const { data: fallbackWords } = useReviewWords(
    (location.state as { sessionType?: string })?.sessionType as 'review' ?? 'review',
    20,
  );

  // Initialize words from navigation state or fetch
  useEffect(() => {
    const stateWords = (location.state as { words?: Word[] })?.words;
    if (stateWords && stateWords.length > 0) {
      setWords(stateWords);
    } else if (fallbackWords?.data && fallbackWords.data.length > 0) {
      setWords(fallbackWords.data);
    }
  }, [location.state, fallbackWords, setWords]);

  // Set session
  useEffect(() => {
    if (sessionId) {
      setSession({ id: sessionId } as never);
    }
  }, [sessionId, setSession]);

  const currentWord = words[currentIndex] ?? null;
  const totalWords = words.length;
  const progress = totalWords > 0 ? ((answers.size) / totalWords) * 100 : 0;
  const isLastWord = currentIndex >= totalWords - 1;

  const handleFlip = useCallback(() => {
    if (!showRating) {
      flipCard();
      setShowRating(true);
      flipTimeRef.current = performance.now();
    }
  }, [showRating, flipCard]);

  const handleRate = useCallback(
    async (quality: ReviewQuality) => {
      if (!currentWord || !sessionId || submitting) return;
      setSubmitting(true);

      try {
        const responseTime = flipTimeRef.current > 0
          ? Math.round(performance.now() - flipTimeRef.current)
          : 0;
        const result = await submitAnswer.mutateAsync({
          word_id: currentWord.id,
          quality,
          response_time_ms: responseTime,
        });
        recordAnswer(currentWord.id, quality);

        // Combo system
        const answerResult = result.data;
        if (answerResult.is_correct) {
          const newCombo = answerResult.combo ?? combo + 1;
          const newMultiplier = answerResult.multiplier ?? 1;
          setCombo(newCombo);
          setMultiplier(newMultiplier);
          if (answerResult.xp_earned) {
            setXpPopup({ xp: answerResult.xp_earned, multiplier: newMultiplier });
          }
        } else {
          if (combo >= 2) {
            setShowComboBreak(true);
          }
          setCombo(0);
          setMultiplier(1);
        }

        if (isLastWord) {
          // Complete session
          await completeSession.mutateAsync(sessionId);
          navigate(`/review/complete/${sessionId}`, {
            state: { totalWords, answers: answers.size + 1 },
          });
          reset();
        } else {
          nextWord();
          setShowRating(false);
          setFlipped(false);
        }
      } catch {
        // Error handled by mutation
      } finally {
        setSubmitting(false);
      }
    },
    [
      currentWord, sessionId, submitting, submitAnswer, recordAnswer, combo,
      isLastWord, completeSession, navigate, totalWords, answers, nextWord,
      setShowRating, setFlipped, reset,
    ],
  );

  const handleQuit = () => {
    if (confirm('Are you sure you want to quit this session?')) {
      if (sessionId && answers.size > 0) {
        completeSession.mutate(sessionId);
      }
      reset();
      navigate('/review');
    }
  };

  // Keyboard shortcuts: Space=flip, 1-5=rate, Escape=quit
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      // Ignore if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      if (e.code === 'Space' || e.key === ' ') {
        e.preventDefault();
        if (!showRating) handleFlip();
      } else if (e.key === 'Escape') {
        handleQuit();
      } else if (showRating && isFlipped) {
        const qualityMap: Record<string, ReviewQuality> = {
          '1': 1,
          '2': 2,
          '3': 3,
          '4': 4,
          '5': 5,
        };
        const quality = qualityMap[e.key];
        if (quality) {
          e.preventDefault();
          handleRate(quality);
        }
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [showRating, isFlipped, handleFlip, handleRate, handleQuit]);

  if (!currentWord || totalWords === 0) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="text-center">
          <h2 className="font-heading text-2xl font-bold">No words to review</h2>
          <p className="mt-2 text-muted-foreground">Add some words first or check back later.</p>
          <Button className="mt-4" onClick={() => navigate('/review')}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Review
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto flex h-full max-w-2xl flex-col">
      {/* Header */}
      <div className="flex items-center justify-between py-4">
        <Button variant="ghost" size="sm" onClick={handleQuit}>
          <X className="mr-1 h-4 w-4" />
          Quit
        </Button>
        <span className="text-sm font-medium text-muted-foreground">
          {currentIndex + 1} / {totalWords}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-6 h-2 overflow-hidden rounded-full bg-muted">
        <motion.div
          className="h-full rounded-full bg-primary"
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>

      {/* Combo Indicator */}
      <div className="mb-4 flex justify-center">
        <ComboIndicator combo={combo} multiplier={multiplier} isActive={combo >= 2} />
      </div>

      {/* Combo Break Effect */}
      {showComboBreak && (
        <ComboBreakEffect onComplete={() => setShowComboBreak(false)} />
      )}

      {/* XP Gain Popup */}
      {xpPopup && (
        <XPGainPopup
          xp={xpPopup.xp}
          multiplier={xpPopup.multiplier}
          onComplete={() => setXpPopup(null)}
        />
      )}

      {/* Card Area */}
      <div className="flex flex-1 flex-col items-center justify-center gap-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentWord.id}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
            className="w-full"
          >
            <FlashCard
              word={currentWord}
              isFlipped={isFlipped}
              onFlip={handleFlip}
            />
          </motion.div>
        </AnimatePresence>

        {/* Quality Rating */}
        <AnimatePresence>
          {showRating && isFlipped && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="w-full"
            >
              <QualityRating onRate={handleRate} disabled={submitting} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Tap hint */}
        {!isFlipped && (
          <motion.p
            className="text-sm text-muted-foreground"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1 }}
          >
            Tap the card or press <kbd className="rounded border border-border bg-muted px-1.5 py-0.5 text-xs font-mono">Space</kbd> to flip
          </motion.p>
        )}

        {/* Keyboard hint when rating */}
        {showRating && isFlipped && (
          <motion.p
            className="text-xs text-muted-foreground text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            Press <kbd className="rounded border border-border bg-muted px-1 py-0.5 text-[10px] font-mono">1</kbd>–
            <kbd className="rounded border border-border bg-muted px-1 py-0.5 text-[10px] font-mono">5</kbd> to rate
          </motion.p>
        )}
      </div>
    </div>
  );
}

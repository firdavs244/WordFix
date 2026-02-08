import { useEffect, useState, useCallback } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { FlashCard, QualityRating } from '../components';
import { useReviewStore } from '@/stores/useReviewStore';
import { useSubmitAnswer, useCompleteSession, useReviewWords } from '../hooks/useReview';
import type { ReviewQuality, Word } from '@/types';

export function ReviewSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const location = useLocation();
  const navigate = useNavigate();
  const [showRating, setShowRating] = useState(false);
  const [submitting, setSubmitting] = useState(false);

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
    }
  }, [showRating, flipCard]);

  const handleRate = useCallback(
    async (quality: ReviewQuality) => {
      if (!currentWord || !sessionId || submitting) return;
      setSubmitting(true);

      try {
        const startTime = performance.now();
        await submitAnswer.mutateAsync({
          word_id: currentWord.id,
          quality,
          response_time_ms: Math.round(performance.now() - startTime),
        });
        recordAnswer(currentWord.id, quality);

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
      currentWord, sessionId, submitting, submitAnswer, recordAnswer,
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
            Tap the card to see the answer
          </motion.p>
        )}
      </div>
    </div>
  );
}

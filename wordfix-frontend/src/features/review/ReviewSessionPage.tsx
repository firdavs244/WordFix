import { useState, useCallback, useRef, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { useReviewStore } from '@/stores/useReviewStore';
import { useSubmitAnswer, useCompleteSession, useReviewWords } from './hooks/useReview';
import SessionTopBar from './components/SessionTopBar';
import SessionProgressBar from './components/SessionProgressBar';
import FlashCardContainer from './components/FlashCardContainer';
import FlashCard from './components/FlashCard';
import QualityRating from './components/QualityRating';
import ComboIndicator from './components/ComboIndicator';
import ComboBreakEffect from './components/ComboBreakEffect';
import XPGainPopup from './components/XPGainPopup';
import type { ReviewQuality, Word } from '@/types';

export default function ReviewSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const flipTimeRef = useRef(0);
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);
  const [showBreak, setShowBreak] = useState(false);
  const [xpGain, setXpGain] = useState<{ xp: number; multiplier: number } | null>(null);

  const { words, currentIndex, isFlipped, setWords, flipCard, setFlipped, recordAnswer, nextWord, reset, isLastWord } = useReviewStore();
  const submitAnswer = useSubmitAnswer(sessionId!);
  const completeSession = useCompleteSession();
  const st = (location.state as { sessionType?: string })?.sessionType as 'review' ?? 'review';
  const { data: fallbackWords } = useReviewWords(st, 20);

  useEffect(() => {
    const sw = (location.state as { words?: Word[] })?.words;
    if (sw?.length) setWords(sw);
    else if (fallbackWords?.data?.length) setWords(fallbackWords.data);
  }, [location.state, fallbackWords, setWords]);

  const handleFlip = useCallback(() => {
    if (!isFlipped) flipTimeRef.current = Date.now();
    flipCard();
  }, [isFlipped, flipCard]);

  const handleRate = useCallback(async (quality: ReviewQuality) => {
    const word = words[currentIndex];
    if (!word) return;
    recordAnswer(word.id, quality);
    try {
      const res = await submitAnswer.mutateAsync({ word_id: word.id, quality, response_time_ms: Date.now() - flipTimeRef.current });
      const r = res.data;
      if (quality < 3 && combo > 1) setShowBreak(true);
      setCombo(r.combo);
      setMultiplier(r.multiplier);
      setXpGain({ xp: r.xp_earned, multiplier: r.multiplier });
      if (isLastWord()) {
        await completeSession.mutateAsync(sessionId!);
        reset();
        navigate(`/review/complete/${sessionId}`, { replace: true });
      } else {
        setTimeout(() => { setFlipped(false); nextWord(); }, 400);
      }
    } catch { /* handled */ }
  }, [words, currentIndex, combo, sessionId, submitAnswer, recordAnswer, completeSession, isLastWord, nextWord, navigate, reset, setFlipped]);

  const handleQuit = useCallback(() => {
    if (confirm('Quit this review session?')) { reset(); navigate('/review'); }
  }, [reset, navigate]);

  const currentWord = words[currentIndex];
  const progress = words.length ? ((currentIndex) / words.length) * 100 : 0;

  if (!currentWord) return <div className="flex min-h-screen items-center justify-center text-muted-foreground">Loading...</div>;

  return (
    <div className="relative min-h-screen bg-background">
      <SessionTopBar currentIndex={currentIndex} total={words.length} onQuit={handleQuit} />
      <SessionProgressBar progress={progress} />
      <ComboIndicator combo={combo} multiplier={multiplier} />
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-8">
        <div className="w-full max-w-xl">
          <FlashCardContainer>
            <FlashCard word={currentWord} isFlipped={isFlipped} onFlip={handleFlip} />
          </FlashCardContainer>
          <AnimatePresence>{isFlipped && <QualityRating onRate={handleRate} />}</AnimatePresence>
        </div>
      </div>
      <AnimatePresence>
        {xpGain && <XPGainPopup xp={xpGain.xp} multiplier={xpGain.multiplier} onDone={() => setXpGain(null)} />}
        {showBreak && <ComboBreakEffect />}
      </AnimatePresence>
    </div>
  );
}

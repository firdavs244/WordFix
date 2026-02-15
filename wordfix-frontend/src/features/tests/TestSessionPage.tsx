import { useState, useCallback } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import TestSessionTopBar from './components/TestSessionTopBar';
import SessionProgressBar from '@/features/review/components/SessionProgressBar';
import ComboIndicator from '@/features/review/components/ComboIndicator';
import XPGainPopup from '@/features/review/components/XPGainPopup';
import TestQuestionCard from './components/TestQuestionCard';
import { useTestSession, useSubmitTestAnswer, useCompleteTest } from './hooks/useTests';
import type { TestQuestion } from '@/types';

export default function TestSessionPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const stateQuestions = (location.state as { questions?: TestQuestion[] })?.questions;

  const { data: testData } = useTestSession(sessionId!);
  const submitAnswer = useSubmitTestAnswer(sessionId!);
  const completeTest = useCompleteTest();

  const questions = stateQuestions ?? testData?.questions ?? [];
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answered, setAnswered] = useState(false);
  const [selectedIdx, setSelectedIdx] = useState<number | undefined>();
  const [correctIdx, setCorrectIdx] = useState<number | undefined>();
  const [feedback, setFeedback] = useState<{ isCorrect: boolean; correctAnswer: string; explanation: string } | null>(null);
  const [combo, setCombo] = useState(0);
  const [multiplier, setMultiplier] = useState(1);
  const [xpGain, setXpGain] = useState<{ xp: number; multiplier: number } | null>(null);

  const total = questions.length;
  const current = questions[currentIndex];
  const progress = total > 0 ? (currentIndex / total) * 100 : 0;
  const isLast = currentIndex >= total - 1;

  const handleAnswer = useCallback(async (answer: string, index?: number) => {
    if (answered || !current) return;
    setAnswered(true);
    if (index !== undefined) setSelectedIdx(index);
    try {
      const res = await submitAnswer.mutateAsync({ question_id: current.id, answer });
      const ci = current.options.indexOf(res.correct_answer);
      if (ci >= 0) setCorrectIdx(ci);
      setFeedback({ isCorrect: res.is_correct, correctAnswer: res.correct_answer, explanation: res.explanation });
      setCombo(res.combo);
      setMultiplier(res.multiplier);
      if (res.xp_earned) setXpGain({ xp: res.xp_earned, multiplier: res.multiplier });
    } catch { /* handled */ }
  }, [answered, current, submitAnswer]);

  const handleNext = useCallback(async () => {
    if (isLast) {
      await completeTest.mutateAsync(sessionId!);
      navigate(`/tests/result/${sessionId}`, { replace: true });
    } else {
      setCurrentIndex((i) => i + 1);
      setAnswered(false);
      setSelectedIdx(undefined);
      setCorrectIdx(undefined);
      setFeedback(null);
    }
  }, [isLast, sessionId, completeTest, navigate]);

  const handleQuit = () => {
    if (confirm('Quit this test?')) navigate('/tests');
  };

  if (!current) {
    return <div className="flex min-h-screen items-center justify-center text-muted-foreground">Loading...</div>;
  }

  return (
    <div className="relative min-h-screen bg-background">
      <TestSessionTopBar current={currentIndex} total={total} onQuit={handleQuit} />
      <SessionProgressBar progress={progress} />
      <ComboIndicator combo={combo} multiplier={multiplier} />
      <div className="flex min-h-[calc(100vh-80px)] items-center justify-center px-4 py-8">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait">
            <TestQuestionCard
              key={currentIndex}
              question={current}
              onAnswer={handleAnswer}
              answered={answered}
              feedback={feedback}
              selectedIndex={selectedIdx}
              correctIndex={correctIdx}
              onNext={handleNext}
              isLast={isLast}
            />
          </AnimatePresence>
        </div>
      </div>
      <AnimatePresence>
        {xpGain && <XPGainPopup xp={xpGain.xp} multiplier={xpGain.multiplier} onDone={() => setXpGain(null)} />}
      </AnimatePresence>
    </div>
  );
}

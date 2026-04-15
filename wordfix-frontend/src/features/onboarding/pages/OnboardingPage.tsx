import { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { useAuthStore } from '@/stores/useAuthStore';
import { useOnboardingQuestions, useSubmitOnboarding, useSkipOnboarding } from '../hooks/useOnboarding';
import { OnboardingBackground } from '../components/OnboardingBackground';
import { OnboardingWelcome } from '../components/OnboardingWelcome';
import { OnboardingQuestionScreen } from '../components/OnboardingQuestion';
import { OnboardingResultScreen } from '../components/OnboardingResult';
import type { OnboardingAnswer, OnboardingResult as ResultType } from '../types';

type Phase = 'welcome' | 'questions' | 'result';

export default function OnboardingPage() {
  const navigate = useNavigate();
  const fetchProfile = useAuthStore((s) => s.fetchProfile);
  const [phase, setPhase] = useState<Phase>('welcome');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<string, string>>(new Map());
  const [selected, setSelected] = useState<string | null>(null);
  const [result, setResult] = useState<ResultType | null>(null);

  const { data: questions, isLoading: loading } = useOnboardingQuestions();
  const submitMutation = useSubmitOnboarding();
  const skipMutation = useSkipOnboarding();

  const list = questions?.data?.questions;
  const current = list?.[currentIndex];
  const total = list?.length || 0;
  const isLast = currentIndex === total - 1;

  const handleNext = useCallback(() => {
    if (!current || !selected) return;
    const next = new Map(answers);
    next.set(current.id, selected);
    setAnswers(next);

    if (!isLast) { setCurrentIndex((i) => i + 1); setSelected(null); return; }

    const payload: OnboardingAnswer[] = Array.from(next.entries()).map(([question_id, answer]) => ({ question_id, answer }));
    submitMutation.mutate(payload, {
      onSuccess: async (data) => { setResult(data.data); setPhase('result'); await fetchProfile().catch(() => {}); },
      onError: () => { toast.error('Failed to submit answers.'); },
    });
  }, [current, selected, answers, isLast, submitMutation, fetchProfile]);

  useEffect(() => {
    if (phase !== 'questions') return;
    const h = (e: KeyboardEvent) => { if (e.key === 'Enter' && selected) handleNext(); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [phase, selected, handleNext]);

  const handleSkip = () => {
    skipMutation.mutate(undefined, {
      onSuccess: async () => {
        await fetchProfile().catch(() => {});
        navigate('/', { replace: true });
      },
      onError: () => { toast.error('Failed to skip onboarding.'); },
    });
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background p-4">
      <OnboardingBackground />
      <div className="relative z-10 w-full max-w-lg">
        <AnimatePresence mode="wait">
          {phase === 'welcome' && (
            <OnboardingWelcome key="w" onStart={() => setPhase('questions')} onSkip={handleSkip} isLoading={loading} totalQuestions={total} />
          )}
          {phase === 'questions' && !current && (
            <div className="flex flex-col items-center justify-center gap-4 py-12">
              <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary border-t-transparent" />
              <p className="text-sm text-muted-foreground">Loading questions...</p>
            </div>
          )}
          {phase === 'questions' && current && (
            <OnboardingQuestionScreen
              key={`q-${currentIndex}`}
              question={current}
              currentIndex={currentIndex}
              totalQuestions={total}
              selectedAnswer={selected}
              selectAnswer={setSelected}
              nextQuestion={handleNext}
              isLastQuestion={isLast}
              isSubmitting={submitMutation.isPending}
            />
          )}
          {phase === 'result' && result && (
            <OnboardingResultScreen key="r" result={result} onContinue={() => navigate('/', { replace: true })} />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

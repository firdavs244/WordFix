import { useState, useCallback, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Brain, ArrowRight, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { useAuthStore } from '@/stores/useAuthStore';
import { useOnboardingQuestions, useSubmitOnboarding, useSkipOnboarding } from '@/features/onboarding/hooks/useOnboarding';
import { OnboardingQuestion } from '@/features/onboarding/components/OnboardingQuestion';
import { OnboardingProgress } from '@/features/onboarding/components/OnboardingProgress';
import { OnboardingResult } from '@/features/onboarding/components/OnboardingResult';
import { SkipButton } from '@/features/onboarding/components/SkipButton';
import type { OnboardingAnswer, OnboardingResult as ResultType } from '@/features/onboarding/types';

type Screen = 'intro' | 'questions' | 'result';

export default function OnboardingPage() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const fetchProfile = useAuthStore((s) => s.fetchProfile);

  const [screen, setScreen] = useState<Screen>('intro');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<string, string>>(new Map());
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [result, setResult] = useState<ResultType | null>(null);

  const { data: questions, isLoading: questionsLoading } = useOnboardingQuestions();
  const submitMutation = useSubmitOnboarding();
  const skipMutation = useSkipOnboarding();

  const questionsList = questions?.data?.questions;
  const currentQuestion = questionsList?.[currentIndex];
  const totalQuestions = questionsList?.length || 0;

  const handleSelect = useCallback((option: string) => {
    setSelectedOption(option);
  }, []);

  const handleNext = useCallback(() => {
    if (!currentQuestion || !selectedOption) return;

    // Save answer
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestion.id, selectedOption);
    setAnswers(newAnswers);

    if (currentIndex < totalQuestions - 1) {
      // Next question
      setCurrentIndex((i) => i + 1);
      setSelectedOption(null);
    } else {
      // Submit all answers
      const answerPayload: OnboardingAnswer[] = Array.from(newAnswers.entries()).map(
        ([question_id, answer]) => ({ question_id, answer }),
      );
      submitMutation.mutate(answerPayload, {
        onSuccess: (data) => {
          setResult(data.data);
          setScreen('result');
          // Refresh profile so has_completed_onboarding updates
          fetchProfile().catch(() => {});
        },
        onError: () => {
          toast.error('Failed to submit answers. Please try again.');
        },
      });
    }
  }, [currentQuestion, selectedOption, answers, currentIndex, totalQuestions, submitMutation, fetchProfile]);

  // Enter key to advance
  useEffect(() => {
    if (screen !== 'questions') return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Enter' && selectedOption) {
        handleNext();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [screen, selectedOption, handleNext]);

  const handleSkip = () => {
    skipMutation.mutate(undefined, {
      onSuccess: () => {
        fetchProfile().catch(() => {});
        navigate('/', { replace: true });
      },
      onError: () => {
        toast.error('Failed to skip onboarding.');
      },
    });
  };

  const handleContinue = () => {
    navigate('/', { replace: true });
  };

  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Top bar */}
      <header className="flex items-center justify-between border-b px-6 py-4">
        <div className="flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-primary" />
          <span className="font-heading text-lg font-bold">WordFix</span>
        </div>
        {screen !== 'result' && (
          <SkipButton onSkip={handleSkip} isLoading={skipMutation.isPending} />
        )}
      </header>

      {/* Content */}
      <main className="flex flex-1 items-center justify-center px-4 py-8">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait">
            {/* INTRO SCREEN */}
            {screen === 'intro' && (
              <motion.div
                key="intro"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -30 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col items-center gap-8 text-center"
              >
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: 'spring', stiffness: 200, damping: 15 }}
                  className="flex h-24 w-24 items-center justify-center rounded-full bg-primary/10"
                >
                  <Brain className="h-12 w-12 text-primary" />
                </motion.div>

                <div className="space-y-3">
                  <h1 className="text-3xl font-bold md:text-4xl">
                    Welcome{user?.full_name ? `, ${user.full_name.split(' ')[0]}` : ''}!
                  </h1>
                  <p className="mx-auto max-w-md text-lg text-muted-foreground">
                    Let's find your English level. This quick test takes about 3-5 minutes and helps us
                    personalize your learning experience.
                  </p>
                </div>

                <div className="grid grid-cols-3 gap-6 text-center">
                  <div className="space-y-1">
                    <p className="text-2xl font-bold text-primary">{totalQuestions || '18'}</p>
                    <p className="text-xs text-muted-foreground">Questions</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-2xl font-bold text-primary">3-5</p>
                    <p className="text-xs text-muted-foreground">Minutes</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-2xl font-bold text-primary">A1-C2</p>
                    <p className="text-xs text-muted-foreground">Levels</p>
                  </div>
                </div>

                <Button
                  size="lg"
                  className="gap-2"
                  onClick={() => setScreen('questions')}
                  disabled={questionsLoading}
                >
                  {questionsLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <ArrowRight className="h-4 w-4" />
                  )}
                  {questionsLoading ? 'Loading...' : 'Start Test'}
                </Button>
              </motion.div>
            )}

            {/* QUESTIONS SCREEN */}
            {screen === 'questions' && currentQuestion && (
              <motion.div
                key="questions"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-8"
              >
                <OnboardingProgress current={currentIndex + 1} total={totalQuestions} />

                <AnimatePresence mode="wait">
                  <OnboardingQuestion
                    key={currentQuestion.id}
                    question={currentQuestion}
                    selectedOption={selectedOption}
                    onSelect={handleSelect}
                    questionNumber={currentIndex + 1}
                  />
                </AnimatePresence>

                <div className="flex justify-end">
                  <Button
                    size="lg"
                    className="gap-2"
                    onClick={handleNext}
                    disabled={!selectedOption || submitMutation.isPending}
                  >
                    {submitMutation.isPending ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : currentIndex === totalQuestions - 1 ? (
                      'Finish'
                    ) : (
                      <>
                        Next
                        <ArrowRight className="h-4 w-4" />
                      </>
                    )}
                  </Button>
                </div>
              </motion.div>
            )}

            {/* RESULT SCREEN */}
            {screen === 'result' && result && (
              <OnboardingResult result={result} onContinue={handleContinue} />
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

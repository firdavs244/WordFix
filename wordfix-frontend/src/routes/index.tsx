import { Routes, Route, Navigate } from 'react-router-dom';
import { Suspense, lazy, useEffect } from 'react';
import { RootLayout } from '@/components/layout/RootLayout';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { LoadingScreen } from '@/components/common/LoadingScreen';
import { useAuthStore } from '@/stores/useAuthStore';
import { NotFoundPage } from '@/components/shared/NotFoundPage';

// Lazy-loaded pages
const LandingPage = lazy(() =>
  import('@/features/landing/pages/LandingPage').then((m) => ({ default: m.LandingPage })),
);
const LoginPage = lazy(() =>
  import('@/features/auth/pages/LoginPage').then((m) => ({ default: m.LoginPage })),
);
const RegisterPage = lazy(() =>
  import('@/features/auth/pages/RegisterPage').then((m) => ({ default: m.RegisterPage })),
);
const DashboardPage = lazy(() =>
  import('@/features/dashboard/pages/DashboardPage').then((m) => ({ default: m.DashboardPage })),
);
const WordsPage = lazy(() =>
  import('@/features/words/pages/WordsPage').then((m) => ({ default: m.WordsPage })),
);
const ProfilePage = lazy(() =>
  import('@/features/profile/pages/ProfilePage').then((m) => ({ default: m.ProfilePage })),
);
const ReviewPage = lazy(() =>
  import('@/features/review/pages/ReviewPage').then((m) => ({ default: m.ReviewPage })),
);
const ReviewSessionPage = lazy(() =>
  import('@/features/review/pages/ReviewSessionPage').then((m) => ({
    default: m.ReviewSessionPage,
  })),
);
const ReviewCompletePage = lazy(() =>
  import('@/features/review/pages/ReviewCompletePage').then((m) => ({
    default: m.ReviewCompletePage,
  })),
);
const ReviewHistoryPage = lazy(() =>
  import('@/features/review/pages/ReviewHistoryPage').then((m) => ({
    default: m.ReviewHistoryPage,
  })),
);
const TestPage = lazy(() => import('@/features/tests/TestPage'));
const TestSessionPage = lazy(() => import('@/features/tests/TestSessionPage'));
const TestResultPage = lazy(() => import('@/features/tests/TestResultPage'));
const GamesPage = lazy(() => import('@/features/games/GamesPage'));
const SpeedRoundPage = lazy(() => import('@/features/games/speed-round/SpeedRoundPage'));
const WordMatchPage = lazy(() => import('@/features/games/word-match/WordMatchPage'));
const WordContextPage = lazy(() => import('@/features/games/word-context/WordContextPage'));
const GameResultPage = lazy(() => import('@/features/games/GameResultPage'));
const StoryBuilderPage = lazy(() => import('@/features/games/story-builder/StoryBuilderPage'));
const ListeningPage = lazy(() => import('@/features/games/listening/ListeningPage'));
const SynonymAntonymPage = lazy(() => import('@/features/games/synonym-antonym/SynonymAntonymPage'));
const IrregularVerbsPage = lazy(() => import('@/features/games/irregular-verbs/IrregularVerbsPage'));
const BadgesPage = lazy(() =>
  import('@/features/progress/pages/BadgesPage').then((m) => ({
    default: m.BadgesPage,
  })),
);
const NotificationsPage = lazy(() =>
  import('@/features/progress/pages/NotificationsPage').then((m) => ({
    default: m.NotificationsPage,
  })),
);
const ImportPage = lazy(() => import('@/features/import/pages/ImportPage'));
const ChatPage = lazy(() =>
  import('@/features/chat/pages/ChatPage').then((m) => ({ default: m.ChatPage })),
);
const ChatSessionPage = lazy(() =>
  import('@/features/chat/pages/ChatSessionPage').then((m) => ({
    default: m.ChatSessionPage,
  })),
);
const ChatHistoryPage = lazy(() =>
  import('@/features/chat/pages/ChatHistoryPage').then((m) => ({
    default: m.ChatHistoryPage,
  })),
);
const AnalyticsPage = lazy(() => import('@/features/analytics/pages/AnalyticsPage'));
const ConfusingPairsPage = lazy(() =>
  import('@/features/confusing-pairs/pages/ConfusingPairsPage').then((m) => ({
    default: m.ConfusingPairsPage,
  })),
);
const OnboardingPage = lazy(() =>
  import('@/features/onboarding/pages/OnboardingPage').then((m) => ({
    default: m.default,
  })),
);
const LearningProfilePage = lazy(() =>
  import('@/features/learning-profile/LearningProfilePage').then((m) => ({
    default: m.LearningProfilePage,
  })),
);
const ImmersivePage = lazy(() => import('@/features/immersive/ImmersivePage'));
const SystemStatusPage = lazy(() =>
  import('@/features/system/pages/SystemStatusPage').then((m) => ({
    default: m.SystemStatusPage,
  })),
);

// ─── Route Guards ──────────────────────────────────────────────────────────────

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  if (isLoading) return <LoadingScreen />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (user && !user.has_completed_onboarding) return <Navigate to="/onboarding" replace />;
  return <>{children}</>;
}

function OnboardingRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, user } = useAuthStore();
  if (isLoading) return <LoadingScreen />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (user?.has_completed_onboarding) return <Navigate to="/" replace />;
  return <>{children}</>;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  if (isLoading) return <LoadingScreen />;
  if (isAuthenticated) return <Navigate to="/" replace />;
  return <>{children}</>;
}

// ─── App Routes ────────────────────────────────────────────────────────────────

export function AppRoutes() {
  const initialize = useAuthStore((s) => s.initialize);

  useEffect(() => {
    initialize();
  }, [initialize]);

  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        {/* Public Routes (no auth required, redirect if logged in) */}
        <Route path="/welcome" element={<LandingPage />} />
        <Route
          element={
            <PublicRoute>
              <AuthLayout />
            </PublicRoute>
          }
        >
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
        </Route>

        {/* Onboarding Route (auth required, not completed yet) */}
        <Route
          path="/onboarding"
          element={
            <OnboardingRoute>
              <OnboardingPage />
            </OnboardingRoute>
          }
        />

        {/* Protected Routes (auth required) */}
        <Route
          element={
            <ProtectedRoute>
              <RootLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<DashboardPage />} />
          <Route path="/words" element={<WordsPage />} />
          <Route path="/review" element={<ReviewPage />} />
          <Route path="/review/session/:sessionId" element={<ReviewSessionPage />} />
          <Route path="/review/complete/:sessionId" element={<ReviewCompletePage />} />
          <Route path="/review/history" element={<ReviewHistoryPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/tests" element={<TestPage />} />
          <Route path="/tests/session/:sessionId" element={<TestSessionPage />} />
          <Route path="/tests/result/:sessionId" element={<TestResultPage />} />
          <Route path="/games" element={<GamesPage />} />
          <Route path="/games/speed-round" element={<SpeedRoundPage />} />
          <Route path="/games/word-match" element={<WordMatchPage />} />
          <Route path="/games/word-context" element={<WordContextPage />} />
          <Route path="/games/story-builder" element={<StoryBuilderPage />} />
          <Route path="/games/listening" element={<ListeningPage />} />
          <Route path="/games/synonym-antonym" element={<SynonymAntonymPage />} />
          <Route path="/games/irregular-verbs" element={<IrregularVerbsPage />} />
          <Route path="/games/result/:sessionId" element={<GameResultPage />} />
          <Route path="/badges" element={<BadgesPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/chat/session/:sessionId" element={<ChatSessionPage />} />
          <Route path="/chat/history" element={<ChatHistoryPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/confusing-pairs" element={<ConfusingPairsPage />} />
          <Route path="/learning-profile" element={<LearningProfilePage />} />
          <Route path="/immersive" element={<ImmersivePage />} />
          <Route path="/system" element={<SystemStatusPage />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}

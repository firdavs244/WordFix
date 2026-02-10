import { Routes, Route, Navigate } from 'react-router-dom';
import { Suspense, lazy, useEffect } from 'react';
import { RootLayout } from '@/components/layout/RootLayout';
import { AuthLayout } from '@/components/layout/AuthLayout';
import { LoadingScreen } from '@/components/common/LoadingScreen';
import { useAuthStore } from '@/stores/useAuthStore';

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
const TestPage = lazy(() =>
  import('@/features/tests/pages/TestPage').then((m) => ({ default: m.TestPage })),
);
const TestSessionPage = lazy(() =>
  import('@/features/tests/pages/TestSessionPage').then((m) => ({
    default: m.TestSessionPage,
  })),
);
const TestResultPage = lazy(() =>
  import('@/features/tests/pages/TestResultPage').then((m) => ({
    default: m.TestResultPage,
  })),
);
const GamesPage = lazy(() =>
  import('@/features/games/pages/GamesPage').then((m) => ({ default: m.GamesPage })),
);
const SpeedRoundPage = lazy(() =>
  import('@/features/games/pages/SpeedRoundPage').then((m) => ({
    default: m.SpeedRoundPage,
  })),
);
const WordMatchPage = lazy(() =>
  import('@/features/games/pages/WordMatchPage').then((m) => ({
    default: m.WordMatchPage,
  })),
);
const WordContextPage = lazy(() =>
  import('@/features/games/pages/WordContextPage').then((m) => ({
    default: m.WordContextPage,
  })),
);
const GameResultPage = lazy(() =>
  import('@/features/games/pages/GameResultPage').then((m) => ({
    default: m.GameResultPage,
  })),
);
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
const ImportPage = lazy(() =>
  import('@/features/import/pages/ImportPage').then((m) => ({ default: m.ImportPage })),
);
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
const AnalyticsPage = lazy(() =>
  import('@/features/analytics/pages/AnalyticsPage').then((m) => ({
    default: m.AnalyticsPage,
  })),
);
const ConfusingPairsPage = lazy(() =>
  import('@/features/confusing-pairs/pages/ConfusingPairsPage').then((m) => ({
    default: m.ConfusingPairsPage,
  })),
);

// ─── Route Guards ──────────────────────────────────────────────────────────────

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  if (isLoading) return <LoadingScreen />;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function PublicRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthStore();
  if (isLoading) return <LoadingScreen />;
  if (isAuthenticated) return <Navigate to="/" replace />;
  return <>{children}</>;
}

// ─── 404 Page ──────────────────────────────────────────────────────────────────

function NotFoundPage() {
  return (
    <div className="flex h-screen flex-col items-center justify-center gap-4">
      <h1 className="font-heading text-6xl font-bold text-primary">404</h1>
      <p className="text-lg text-muted-foreground">Page not found</p>
      <a href="/" className="text-primary hover:underline">
        Go Home
      </a>
    </div>
  );
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
          <Route path="/games/result/:sessionId" element={<GameResultPage />} />
          <Route path="/badges" element={<BadgesPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/chat/session/:sessionId" element={<ChatSessionPage />} />
          <Route path="/chat/history" element={<ChatHistoryPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/confusing-pairs" element={<ConfusingPairsPage />} />
        </Route>

        {/* 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
}

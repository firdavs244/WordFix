import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { LearningProfilePage } from '../LearningProfilePage';

vi.mock('../hooks/useLearningProfile', () => ({
  useLearningProfileData: () => ({
    profile: {
      preferred_style: 'visual',
      style_confidence: 0.85,
      best_time: { start_hour: 9, end_hour: 11, best_days: [0, 2, 4] },
      session_stats: { avg_duration: 15, optimal_words: 20, retention_rate: 0.78 },
      skills: {
        strongest: ['vocabulary'],
        weakest: ['listening'],
        scores: { reading: 80, vocabulary: 90, listening: 40, context: 60, speed: 70 },
      },
      difficulty_level: 3,
      last_analyzed: new Date().toISOString(),
    },
    profileLoading: false,
    hasAnalyzed: true,
    mistakes: [],
    mistakesLoading: false,
    recommendations: [],
    recsLoading: false,
    coverage: null,
    coverageLoading: false,
    analyze: vi.fn(),
    analyzeIsPending: false,
    acceptRecommendation: vi.fn(),
    acceptIsPending: false,
  }),
}));

describe('LearningProfilePage', () => {
  it('renders the page header', () => {
    render(<LearningProfilePage />);
    expect(screen.getByText('Learning Profile')).toBeInTheDocument();
  });

  it('renders the analyze button', () => {
    render(<LearningProfilePage />);
    expect(screen.getByText('Analyze Profile')).toBeInTheDocument();
  });

  it('renders learning style card', () => {
    render(<LearningProfilePage />);
    expect(screen.getByText('Learning Style')).toBeInTheDocument();
  });

  it('renders skills card', () => {
    render(<LearningProfilePage />);
    expect(screen.getByText('Skills')).toBeInTheDocument();
  });
});

// ─── Learning Profile Types ────────────────────────────────────────────────────

export interface LearningProfile {
  preferred_style: 'visual' | 'auditory' | 'reading' | 'kinesthetic';
  style_confidence: number;
  best_time: {
    start_hour: number;
    end_hour: number;
    best_days: number[];
  };
  session_stats: {
    avg_duration: number;
    optimal_words: number;
    retention_rate: number;
  };
  skills: {
    strongest: string[];
    weakest: string[];
    scores?: Record<string, number>;
  };
  difficulty_level: number;
  last_analyzed: string | null;
}

export interface AnalyzeResult {
  learning_style: {
    style: string;
    confidence: number;
    breakdown: Record<string, number>;
  };
  optimal_time: {
    best_hours: number[];
    best_days: number[];
    confidence: number;
  };
  skills: {
    strongest: string[];
    weakest: string[];
    scores: Record<string, number>;
  };
  recommendations: string[];
}

export interface MistakePattern {
  id: string;
  type: string;
  description: string;
  examples: Array<{ wrong: string; correct: string; context: string }>;
  occurrence_count: number;
  is_resolved: boolean;
  related_words: string[];
}

export interface WordRecommendation {
  id: string;
  word: string;
  translation: string;
  reason: string;
  reason_type: 'domain_gap' | 'confusion_fix' | 'level_appropriate' | 'high_frequency';
  priority: number;
  is_accepted?: boolean;
  ai_confidence?: number;
}

export interface DomainCoverage {
  [domain: string]: {
    total: number;
    coverage: number;
    mastered: number;
  };
}

export interface DifficultyInfo {
  difficulty_level: number;
  adjusted: boolean;
  direction: 'up' | 'down' | 'stable';
}

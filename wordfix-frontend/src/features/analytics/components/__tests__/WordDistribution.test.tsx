import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import WordDistribution from '../../components/WordDistribution';
import type { WordProgressData } from '@/types';

const data: WordProgressData = {
  by_confidence: { mastered: 15, confident: 10, learning: 20, new: 5 },
  by_difficulty: { easy: 20, medium: 20, hard: 10 },
  by_category: [],
  recently_mastered: [],
  needs_attention: [],
};

describe('WordDistribution', () => {
  it('renders confidence chart', () => {
    render(<WordDistribution data={data} />);
    expect(screen.getByText('By Confidence')).toBeInTheDocument();
  });

  it('renders difficulty distribution', () => {
    render(<WordDistribution data={data} />);
    expect(screen.getByText('By Difficulty')).toBeInTheDocument();
  });

  it('shows confidence labels', () => {
    render(<WordDistribution data={data} />);
    expect(screen.getByText('mastered')).toBeInTheDocument();
    expect(screen.getByText('learning')).toBeInTheDocument();
  });

  it('shows difficulty labels', () => {
    render(<WordDistribution data={data} />);
    expect(screen.getByText('easy')).toBeInTheDocument();
    expect(screen.getByText('hard')).toBeInTheDocument();
  });
});

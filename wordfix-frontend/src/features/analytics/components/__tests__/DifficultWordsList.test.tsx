import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import DifficultWordsList from '../../components/DifficultWordsList';
import type { DifficultWord } from '@/types';

const words: DifficultWord[] = [
  { id: 'w3', original_word: 'difficult', translation: 'difícil', accuracy_rate: 25, review_count: 8, incorrect_count: 6, confidence_score: 0.2 },
  { id: 'w4', original_word: 'elaborate', translation: 'elaborar', accuracy_rate: 33, review_count: 6, incorrect_count: 4, confidence_score: 0.3 },
];

describe('DifficultWordsList', () => {
  it('renders heading', () => {
    render(<DifficultWordsList words={words} />);
    expect(screen.getByText('Needs Attention')).toBeInTheDocument();
  });

  it('shows word count badge', () => {
    render(<DifficultWordsList words={words} />);
    const matches = screen.getAllByText('2');
    expect(matches.length).toBeGreaterThanOrEqual(1);
  });

  it('renders word items', () => {
    render(<DifficultWordsList words={words} />);
    expect(screen.getByText('difficult')).toBeInTheDocument();
    expect(screen.getByText('elaborate')).toBeInTheDocument();
  });

  it('shows accuracy percentage', () => {
    render(<DifficultWordsList words={words} />);
    expect(screen.getByText('25%')).toBeInTheDocument();
    expect(screen.getByText('33%')).toBeInTheDocument();
  });

  it('returns null when empty', () => {
    const { container } = render(<DifficultWordsList words={[]} />);
    expect(container.innerHTML).toBe('');
  });
});

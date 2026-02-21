import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import TextImportReview from '../../components/TextImportReview';
import type { WordSuggestion } from '@/types';

const words: WordSuggestion[] = [
  { word: 'adventure', translation: 'приключение', part_of_speech: 'noun', context_sentence: 'Great adventure.', difficulty: 'medium', reason: 'Common word' },
  { word: 'journey', translation: 'путешествие', part_of_speech: 'noun', context_sentence: 'Long journey.', difficulty: 'easy', reason: 'Travel word' },
];

describe('TextImportReview', () => {
  const props = {
    words,
    selectedIds: new Set([0]),
    onToggle: vi.fn(),
    onSelectAll: vi.fn(),
    onDeselectAll: vi.fn(),
    onImport: vi.fn(),
    isImporting: false,
  };

  it('shows word count', () => {
    render(<TextImportReview {...props} />);
    expect(screen.getByText('Found 2 words')).toBeInTheDocument();
  });

  it('shows selected count', () => {
    render(<TextImportReview {...props} />);
    expect(screen.getByText('1 selected')).toBeInTheDocument();
  });

  it('renders select/deselect all buttons', () => {
    render(<TextImportReview {...props} />);
    expect(screen.getByText('Select All')).toBeInTheDocument();
    expect(screen.getByText('Deselect All')).toBeInTheDocument();
  });

  it('calls onSelectAll when clicked', async () => {
    const user = userEvent.setup();
    render(<TextImportReview {...props} />);
    await user.click(screen.getByText('Select All'));
    expect(props.onSelectAll).toHaveBeenCalled();
  });

  it('renders import button with count', () => {
    render(<TextImportReview {...props} />);
    expect(screen.getByText('Import 1 Words')).toBeInTheDocument();
  });
});

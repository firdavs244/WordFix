import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import CSVPreview from '../../components/CSVPreview';
import type { CSVValidateResult } from '@/types';

const data: CSVValidateResult = {
  headers: ['word', 'translation', 'difficulty'],
  preview: [
    { word: 'apple', translation: 'яблоко', difficulty: 'easy' },
    { word: 'banana', translation: 'банан', difficulty: 'easy' },
  ],
  total_rows: 10,
  valid_rows: 9,
  errors: ['Row 5: missing translation'],
  has_translation: true,
  has_difficulty: true,
  has_category: false,
};

describe('CSVPreview', () => {
  const onImport = vi.fn();

  it('shows row count', () => {
    render(<CSVPreview data={data} onImport={onImport} isImporting={false} />);
    expect(screen.getByText('10 rows detected')).toBeInTheDocument();
  });

  it('renders table headers', () => {
    render(<CSVPreview data={data} onImport={onImport} isImporting={false} />);
    expect(screen.getByText('word')).toBeInTheDocument();
    expect(screen.getByText('translation')).toBeInTheDocument();
  });

  it('renders preview data', () => {
    render(<CSVPreview data={data} onImport={onImport} isImporting={false} />);
    expect(screen.getByText('apple')).toBeInTheDocument();
    expect(screen.getByText('banana')).toBeInTheDocument();
  });

  it('shows errors', () => {
    render(<CSVPreview data={data} onImport={onImport} isImporting={false} />);
    expect(screen.getByText('Row 5: missing translation')).toBeInTheDocument();
  });

  it('shows import button with valid count', () => {
    render(<CSVPreview data={data} onImport={onImport} isImporting={false} />);
    expect(screen.getByText('Import 9 Words')).toBeInTheDocument();
  });
});

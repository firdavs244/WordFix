import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import CSVDropZone from '../../components/CSVDropZone';

describe('CSVDropZone', () => {
  const onFileSelect = vi.fn();

  it('renders drop zone text', () => {
    render(<CSVDropZone selectedFile={null} onFileSelect={onFileSelect} />);
    expect(screen.getByText(/drag.*drop/i)).toBeInTheDocument();
  });

  it('shows file name when file is set', () => {
    const file = new File(['col1,col2'], 'words.csv', { type: 'text/csv' });
    render(<CSVDropZone selectedFile={file} onFileSelect={onFileSelect} />);
    expect(screen.getByText('words.csv')).toBeInTheDocument();
  });
});

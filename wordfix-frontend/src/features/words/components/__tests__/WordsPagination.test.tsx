import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import WordsPagination from '../WordsPagination';

describe('WordsPagination', () => {
  const onPageChange = vi.fn();

  beforeEach(() => {
    onPageChange.mockClear();
  });

  it('renders page numbers for small total', () => {
    render(<WordsPagination currentPage={1} totalPages={3} onPageChange={onPageChange} />);
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });

  it('disables previous button on first page', () => {
    render(<WordsPagination currentPage={1} totalPages={5} onPageChange={onPageChange} />);
    expect(screen.getByLabelText('Previous page')).toBeDisabled();
  });

  it('disables next button on last page', () => {
    render(<WordsPagination currentPage={5} totalPages={5} onPageChange={onPageChange} />);
    expect(screen.getByLabelText('Next page')).toBeDisabled();
  });

  it('calls onPageChange when a page number is clicked', async () => {
    const user = userEvent.setup();
    render(<WordsPagination currentPage={1} totalPages={5} onPageChange={onPageChange} />);
    await user.click(screen.getByText('2'));
    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it('calls onPageChange with next page when next is clicked', async () => {
    const user = userEvent.setup();
    render(<WordsPagination currentPage={2} totalPages={5} onPageChange={onPageChange} />);
    await user.click(screen.getByLabelText('Next page'));
    expect(onPageChange).toHaveBeenCalledWith(3);
  });

  it('calls onPageChange with previous page when previous is clicked', async () => {
    const user = userEvent.setup();
    render(<WordsPagination currentPage={3} totalPages={5} onPageChange={onPageChange} />);
    await user.click(screen.getByLabelText('Previous page'));
    expect(onPageChange).toHaveBeenCalledWith(2);
  });

  it('renders ellipsis for large page ranges', () => {
    render(<WordsPagination currentPage={5} totalPages={10} onPageChange={onPageChange} />);
    const ellipses = screen.getAllByText('…');
    expect(ellipses.length).toBeGreaterThanOrEqual(1);
  });

  it('highlights current page', () => {
    render(<WordsPagination currentPage={2} totalPages={5} onPageChange={onPageChange} />);
    const currentBtn = screen.getByText('2');
    expect(currentBtn.className).toContain('bg-primary');
  });
});

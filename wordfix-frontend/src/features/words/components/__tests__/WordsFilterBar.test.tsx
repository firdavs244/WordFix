import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import WordsFilterBar from '../WordsFilterBar';
import type { WordsFiltersState } from '../../WordsPage';

vi.mock('../WordsSegmentedControl', () => ({
  default: ({ value, onChange }: { value: string; onChange: (v: string) => void }) => (
    <div data-testid="segmented-control">
      <button data-testid="select-easy" onClick={() => onChange('easy')}>Easy</button>
      <span data-testid="current-value">{value}</span>
    </div>
  ),
}));
vi.mock('../WordsViewToggle', () => ({
  default: ({ view }: { view: string }) => <div data-testid="view-toggle">{view}</div>,
}));

function setup(overrides?: Partial<WordsFiltersState>) {
  const filters: WordsFiltersState = { search: '', difficulty: 'all', page: 1, ...overrides };
  const onFiltersChange = vi.fn();
  const onViewChange = vi.fn();
  const result = render(
    <WordsFilterBar filters={filters} onFiltersChange={onFiltersChange} view="grid" onViewChange={onViewChange} />,
  );
  return { ...result, onFiltersChange, onViewChange, filters };
}

describe('WordsFilterBar', () => {
  it('renders search input', () => {
    setup();
    expect(screen.getByPlaceholderText('Search words...')).toBeInTheDocument();
  });

  it('renders segmented control and view toggle', () => {
    setup();
    expect(screen.getByTestId('segmented-control')).toBeInTheDocument();
    expect(screen.getByTestId('view-toggle')).toBeInTheDocument();
  });

  it('calls onFiltersChange when typing in search', async () => {
    const user = userEvent.setup();
    const { onFiltersChange } = setup();
    await user.type(screen.getByPlaceholderText('Search words...'), 'a');
    expect(onFiltersChange).toHaveBeenCalledWith(expect.objectContaining({ search: 'a', page: 1 }));
  });

  it('shows clear button when search has value', () => {
    setup({ search: 'hello' });
    expect(screen.getByLabelText('Clear search')).toBeInTheDocument();
  });

  it('does not show clear button when search is empty', () => {
    setup({ search: '' });
    expect(screen.queryByLabelText('Clear search')).not.toBeInTheDocument();
  });

  it('clears search when clear button is clicked', async () => {
    const user = userEvent.setup();
    const { onFiltersChange } = setup({ search: 'hello' });
    await user.click(screen.getByLabelText('Clear search'));
    expect(onFiltersChange).toHaveBeenCalledWith(expect.objectContaining({ search: '', page: 1 }));
  });

  it('calls onFiltersChange when difficulty changes via segmented control', async () => {
    const user = userEvent.setup();
    const { onFiltersChange } = setup();
    await user.click(screen.getByTestId('select-easy'));
    expect(onFiltersChange).toHaveBeenCalledWith(expect.objectContaining({ difficulty: 'easy', page: 1 }));
  });

  it('displays current search value in input', () => {
    setup({ search: 'test' });
    expect(screen.getByPlaceholderText('Search words...')).toHaveValue('test');
  });
});

import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent, waitFor } from '@/test/utils';
import WordsPage from '../../WordsPage';

// Mock child components to isolate page composition
vi.mock('../WordsHeader', () => ({ default: () => <div data-testid="words-header">Header</div> }));
vi.mock('../WordsStatsBar', () => ({ default: () => <div data-testid="words-stats-bar">Stats</div> }));
vi.mock('../WordsFilterBar', () => ({
  default: ({ view, onViewChange }: { view: string; onViewChange: (v: 'grid' | 'list') => void }) => (
    <div data-testid="words-filter-bar">
      <button data-testid="toggle-view" onClick={() => onViewChange(view === 'grid' ? 'list' : 'grid')}>
        Toggle {view}
      </button>
    </div>
  ),
}));
vi.mock('../WordsGrid', () => ({ default: () => <div data-testid="words-grid">Grid</div> }));
vi.mock('../WordsList', () => ({ default: () => <div data-testid="words-list">List</div> }));

describe('WordsPage', () => {
  it('renders header, stats bar, filter bar and grid by default', () => {
    render(<WordsPage />);
    expect(screen.getByTestId('words-header')).toBeInTheDocument();
    expect(screen.getByTestId('words-stats-bar')).toBeInTheDocument();
    expect(screen.getByTestId('words-filter-bar')).toBeInTheDocument();
    expect(screen.getByTestId('words-grid')).toBeInTheDocument();
  });

  it('defaults to grid view', () => {
    render(<WordsPage />);
    expect(screen.getByTestId('words-grid')).toBeInTheDocument();
    expect(screen.queryByTestId('words-list')).not.toBeInTheDocument();
  });

  it('switches to list view when toggled', async () => {
    const user = userEvent.setup();
    render(<WordsPage />);
    await user.click(screen.getByTestId('toggle-view'));
    expect(screen.getByTestId('words-list')).toBeInTheDocument();
    expect(screen.queryByTestId('words-grid')).not.toBeInTheDocument();
  });

  it('switches back to grid view on second toggle', async () => {
    const user = userEvent.setup();
    render(<WordsPage />);
    await user.click(screen.getByTestId('toggle-view'));
    await user.click(screen.getByTestId('toggle-view'));
    expect(screen.getByTestId('words-grid')).toBeInTheDocument();
  });
});

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import BadgesPage from '../../BadgesPage';

vi.mock('../../components/BadgesProgress', () => ({ default: () => <div data-testid="badges-progress" /> }));
vi.mock('../../components/BadgesCategoryFilter', () => ({ default: ({ activeCategory, onChange }: any) => (
  <div data-testid="category-filter">
    <button onClick={() => onChange('words')}>Words</button>
    <span>{activeCategory}</span>
  </div>
) }));
vi.mock('../../components/BadgesGrid', () => ({ default: ({ category }: any) => <div data-testid="badges-grid">{category}</div> }));

describe('BadgesPage', () => {
  it('renders page header with "Badges & Achievements"', () => {
    render(<BadgesPage />);
    expect(screen.getByText('Badges & Achievements')).toBeInTheDocument();
  });

  it('renders badges progress bar', () => {
    render(<BadgesPage />);
    expect(screen.getByTestId('badges-progress')).toBeInTheDocument();
  });

  it('renders category filter chips', () => {
    render(<BadgesPage />);
    expect(screen.getByTestId('category-filter')).toBeInTheDocument();
  });

  it('renders badge grid', () => {
    render(<BadgesPage />);
    expect(screen.getByTestId('badges-grid')).toBeInTheDocument();
  });

  it('filters badges by category when chip clicked', async () => {
    const { userEvent } = await import('@/test/utils');
    const user = userEvent.setup();
    render(<BadgesPage />);
    await user.click(screen.getByText('Words'));
    expect(screen.getByTestId('badges-grid')).toHaveTextContent('words');
  });

  it('starts with "All" selected by default', () => {
    render(<BadgesPage />);
    expect(screen.getByTestId('badges-grid')).toHaveTextContent('all');
  });
});

import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ProficiencyLevelSelector from '../ProficiencyLevelSelector';

describe('ProficiencyLevelSelector', () => {
  it('renders all 6 level buttons', () => {
    render(<ProficiencyLevelSelector value="B1" onChange={vi.fn()} />);
    expect(screen.getByText('A1')).toBeInTheDocument();
    expect(screen.getByText('A2')).toBeInTheDocument();
    expect(screen.getByText('B1')).toBeInTheDocument();
    expect(screen.getByText('B2')).toBeInTheDocument();
    expect(screen.getByText('C1')).toBeInTheDocument();
    expect(screen.getByText('C2')).toBeInTheDocument();
  });

  it('highlights active level', () => {
    render(<ProficiencyLevelSelector value="B2" onChange={vi.fn()} />);
    const b2Text = screen.getByText('B2');
    expect(b2Text).toHaveClass('text-white');
  });

  it('calls onChange when level clicked', async () => {
    const onChange = vi.fn();
    const user = userEvent.setup();
    render(<ProficiencyLevelSelector value="B1" onChange={onChange} />);
    await user.click(screen.getByText('C1'));
    expect(onChange).toHaveBeenCalledWith('C1');
  });

  it('renders A1 through C2 labels', () => {
    render(<ProficiencyLevelSelector value="A1" onChange={vi.fn()} />);
    const labels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
    for (const label of labels) {
      expect(screen.getByText(label)).toBeInTheDocument();
    }
  });
});

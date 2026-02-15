import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import AttemptIndicator from '../AttemptIndicator';

describe('AttemptIndicator', () => {
  it('renders the indicator', () => {
    render(<AttemptIndicator total={3} remaining={2} />);
    expect(screen.getByTestId('attempt-indicator')).toBeInTheDocument();
  });

  it('displays remaining count text', () => {
    render(<AttemptIndicator total={3} remaining={2} />);
    expect(screen.getByText('2 left')).toBeInTheDocument();
  });

  it('renders correct number of dots', () => {
    const { container } = render(<AttemptIndicator total={3} remaining={2} />);
    const dots = container.querySelectorAll('.rounded-full');
    expect(dots).toHaveLength(3);
  });

  it('updates remaining text when changed', () => {
    const { rerender } = render(<AttemptIndicator total={3} remaining={3} />);
    expect(screen.getByText('3 left')).toBeInTheDocument();
    rerender(<AttemptIndicator total={3} remaining={1} />);
    expect(screen.getByText('1 left')).toBeInTheDocument();
  });
});

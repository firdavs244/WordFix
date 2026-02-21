import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { DrillModal } from '../../components/DrillModal';

describe('DrillModal', () => {
  it('renders nothing when not open', () => {
    const { container } = render(<DrillModal pairId="cp-1" isOpen={false} onClose={vi.fn()} />);
    expect(container.innerHTML).toBe('');
  });

  it('shows loading state when open', () => {
    render(<DrillModal pairId="cp-1" isOpen={true} onClose={vi.fn()} />);
    expect(screen.getByText(/generating drill/i)).toBeInTheDocument();
  });

  it('shows explanation after loading', async () => {
    render(<DrillModal pairId="cp-1" isOpen={true} onClose={vi.fn()} />);
    await waitFor(() => {
      expect(screen.getByText(/understanding the difference/i)).toBeInTheDocument();
    });
  });

  it('renders close button', () => {
    render(<DrillModal pairId="cp-1" isOpen={true} onClose={vi.fn()} />);
    expect(screen.getByText('✕')).toBeInTheDocument();
  });
});

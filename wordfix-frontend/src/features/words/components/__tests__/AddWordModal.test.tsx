import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent, waitFor } from '@/test/utils';
import AddWordModal from '../AddWordModal';

// Mock AddWordForm so we can test the modal wrapper in isolation
vi.mock('../AddWordForm', () => ({
  default: ({ onSuccess }: { onSuccess: () => void }) => (
    <div data-testid="add-word-form">
      <button data-testid="trigger-success" onClick={onSuccess}>Done</button>
    </div>
  ),
}));

describe('AddWordModal', () => {
  const onClose = vi.fn();

  beforeEach(() => {
    onClose.mockClear();
  });

  it('renders modal dialog', () => {
    render(<AddWordModal onClose={onClose} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('has aria-modal and aria-label attributes', () => {
    render(<AddWordModal onClose={onClose} />);
    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-label', 'Add New Word');
  });

  it('renders the title "Add New Word"', () => {
    render(<AddWordModal onClose={onClose} />);
    expect(screen.getByText('Add New Word')).toBeInTheDocument();
  });

  it('renders close button', () => {
    render(<AddWordModal onClose={onClose} />);
    expect(screen.getByLabelText('Close')).toBeInTheDocument();
  });

  it('calls onClose when close button clicked', async () => {
    const user = userEvent.setup();
    render(<AddWordModal onClose={onClose} />);
    await user.click(screen.getByLabelText('Close'));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when backdrop clicked', async () => {
    const user = userEvent.setup();
    render(<AddWordModal onClose={onClose} />);
    await user.click(screen.getByRole('dialog'));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when Escape key pressed', async () => {
    const user = userEvent.setup();
    render(<AddWordModal onClose={onClose} />);
    await user.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('renders AddWordForm component', () => {
    render(<AddWordModal onClose={onClose} />);
    expect(screen.getByTestId('add-word-form')).toBeInTheDocument();
  });

  it('calls onClose when form triggers success', async () => {
    const user = userEvent.setup();
    render(<AddWordModal onClose={onClose} />);
    await user.click(screen.getByTestId('trigger-success'));
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('sets body overflow hidden on mount and restores on unmount', () => {
    const { unmount } = render(<AddWordModal onClose={onClose} />);
    expect(document.body.style.overflow).toBe('hidden');
    unmount();
    expect(document.body.style.overflow).toBe('');
  });
});

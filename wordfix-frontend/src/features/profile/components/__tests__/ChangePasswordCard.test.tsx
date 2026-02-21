import { describe, it, expect } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import ChangePasswordCard from '../ChangePasswordCard';

describe('ChangePasswordCard', () => {
  it('renders three password fields', () => {
    render(<ChangePasswordCard />);
    expect(screen.getByText('Current Password')).toBeInTheDocument();
    expect(screen.getByText('New Password')).toBeInTheDocument();
    expect(screen.getByText('Confirm New Password')).toBeInTheDocument();
  });

  it('renders change password button', () => {
    render(<ChangePasswordCard />);
    expect(screen.getByText('Change Password')).toBeInTheDocument();
  });

  it('renders security header', () => {
    render(<ChangePasswordCard />);
    expect(screen.getByText('Security')).toBeInTheDocument();
  });

  it('shows validation errors for short password', async () => {
    const user = userEvent.setup();
    render(<ChangePasswordCard />);
    // Fill the new password fields with a short value
    const inputs = screen.getAllByPlaceholderText(/password/i);
    if (inputs[1]) {
      await user.type(inputs[1], 'short');
    }
    await user.click(screen.getByText('Change Password'));
    expect(screen.getByText('Password must be at least 8 characters')).toBeInTheDocument();
  });

  it('shows mismatch error when passwords differ', async () => {
    const user = userEvent.setup();
    render(<ChangePasswordCard />);
    const inputs = screen.getAllByPlaceholderText(/password/i);
    if (inputs[1]) await user.type(inputs[1], 'password123');
    if (inputs[2]) await user.type(inputs[2], 'different123');
    await user.click(screen.getByText('Change Password'));
    expect(screen.getByText('Passwords do not match')).toBeInTheDocument();
  });
});

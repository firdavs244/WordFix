import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, userEvent, waitFor } from '@/test/utils';
import { useAuthStore } from '@/stores/useAuthStore';
import ProfileEditForm from '../ProfileEditForm';

describe('ProfileEditForm', () => {
  const onCancel = vi.fn();

  beforeEach(() => {
    onCancel.mockClear();
    useAuthStore.setState({
      user: {
        id: 'u1', email: 'test@example.com', username: 'testuser', full_name: 'Test User',
        avatar: '', native_language: 'uz', learning_language: 'en', proficiency_level: 'B1',
        daily_goal: 10, timezone: 'UTC', is_premium: false, premium_until: null,
        is_premium_active: false, is_active: true, date_joined: '2025-01-01',
        last_login: null, has_completed_onboarding: true,
      },
      isAuthenticated: true,
    });
  });

  it('renders full name input with current value', () => {
    render(<ProfileEditForm onCancel={onCancel} />);
    const input = screen.getByPlaceholderText('Your full name') as HTMLInputElement;
    expect(input.value).toBe('Test User');
  });

  it('renders daily goal slider', () => {
    render(<ProfileEditForm onCancel={onCancel} />);
    expect(screen.getByLabelText('Daily Goal')).toBeInTheDocument();
  });

  it('renders proficiency level selector', () => {
    render(<ProfileEditForm onCancel={onCancel} />);
    expect(screen.getByText('Proficiency Level')).toBeInTheDocument();
  });

  it('cancels edit on cancel button click', async () => {
    const user = userEvent.setup();
    render(<ProfileEditForm onCancel={onCancel} />);
    await user.click(screen.getByText('Cancel'));
    expect(onCancel).toHaveBeenCalled();
  });

  it('submits form with updated data', async () => {
    const user = userEvent.setup();
    render(<ProfileEditForm onCancel={onCancel} />);
    await user.click(screen.getByText('Save Changes'));
    await waitFor(() => expect(onCancel).toHaveBeenCalled());
  });
});

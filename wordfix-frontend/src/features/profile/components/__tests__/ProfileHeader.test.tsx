import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@/test/utils';
import { useAuthStore } from '@/stores/useAuthStore';
import ProfileHeader from '../ProfileHeader';

describe('ProfileHeader', () => {
  beforeEach(() => {
    useAuthStore.setState({
      user: {
        id: 'u1', email: 'john@example.com', username: 'john', full_name: 'John Doe',
        avatar: '', native_language: 'uz', learning_language: 'en', proficiency_level: 'B1',
        daily_goal: 10, timezone: 'UTC', is_premium: false, premium_until: null,
        is_premium_active: false, is_active: true, date_joined: '2025-01-01',
        last_login: null, has_completed_onboarding: true,
      },
      isAuthenticated: true,
    });
  });

  it('renders user avatar with first letter', () => {
    render(<ProfileHeader />);
    expect(screen.getByText('J')).toBeInTheDocument();
  });

  it('renders full name', () => {
    render(<ProfileHeader />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('renders email', () => {
    render(<ProfileHeader />);
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });

  it('renders level badge', () => {
    render(<ProfileHeader />);
    expect(screen.getByText('B1')).toBeInTheDocument();
  });

  it('renders gradient banner', () => {
    const { container } = render(<ProfileHeader />);
    expect(container.querySelector('.h-24')).toBeInTheDocument();
  });
});

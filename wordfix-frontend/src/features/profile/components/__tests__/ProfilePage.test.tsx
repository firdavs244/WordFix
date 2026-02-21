import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import { ProfilePage } from '../../pages/ProfilePage';

vi.mock('../../components/ProfileHeader', () => ({ default: () => <div data-testid="profile-header">Header</div> }));
vi.mock('../../components/ProfileInfoCard', () => ({ default: () => <div data-testid="profile-info">Info</div> }));
vi.mock('../../components/ChangePasswordCard', () => ({ default: () => <div data-testid="change-password">Password</div> }));
vi.mock('../../components/LearningLevelCard', () => ({ default: () => <div data-testid="learning-level">Level</div> }));

describe('ProfilePage', () => {
  it('renders profile header with avatar', () => {
    render(<ProfilePage />);
    expect(screen.getByTestId('profile-header')).toBeInTheDocument();
  });

  it('renders personal info card', () => {
    render(<ProfilePage />);
    expect(screen.getByTestId('profile-info')).toBeInTheDocument();
  });

  it('renders change password card', () => {
    render(<ProfilePage />);
    expect(screen.getByTestId('change-password')).toBeInTheDocument();
  });

  it('renders learning level card', () => {
    render(<ProfilePage />);
    expect(screen.getByTestId('learning-level')).toBeInTheDocument();
  });
});

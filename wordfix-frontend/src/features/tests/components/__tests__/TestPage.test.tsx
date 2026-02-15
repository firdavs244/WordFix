import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@/test/utils';
import TestPage from '../../TestPage';

vi.mock('../TestConfigPanel', () => ({ default: () => <div data-testid="test-config-panel">Config</div> }));
vi.mock('../RecentTestsList', () => ({ default: () => <div data-testid="recent-tests-list">Recent</div> }));

describe('TestPage', () => {
  it('renders page header with "AI Test Generator"', () => {
    render(<TestPage />);
    expect(screen.getByText('AI Test Generator')).toBeInTheDocument();
  });

  it('renders description text', () => {
    render(<TestPage />);
    expect(screen.getByText('Generate personalized vocabulary tests')).toBeInTheDocument();
  });

  it('renders AI-Powered badge', () => {
    render(<TestPage />);
    expect(screen.getByText('AI-Powered')).toBeInTheDocument();
  });

  it('renders TestConfigPanel component', () => {
    render(<TestPage />);
    expect(screen.getByTestId('test-config-panel')).toBeInTheDocument();
  });

  it('renders RecentTestsList component', () => {
    render(<TestPage />);
    expect(screen.getByTestId('recent-tests-list')).toBeInTheDocument();
  });
});

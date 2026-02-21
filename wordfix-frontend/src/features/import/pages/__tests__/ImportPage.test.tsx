import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import ImportPage from '../../pages/ImportPage';

describe('ImportPage', () => {
  it('renders page title', () => {
    render(<ImportPage />);
    expect(screen.getByText('Smart Import')).toBeInTheDocument();
  });

  it('renders tab options', () => {
    render(<ImportPage />);
    expect(screen.getByText('From Text')).toBeInTheDocument();
    expect(screen.getByText('From CSV')).toBeInTheDocument();
  });
});

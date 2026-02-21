import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import { NotFoundPage } from '../NotFoundPage';

describe('NotFoundPage', () => {
  it('renders 404 text', () => {
    render(<NotFoundPage />);
    expect(screen.getByText('404')).toBeInTheDocument();
  });

  it('renders page not found heading', () => {
    render(<NotFoundPage />);
    expect(screen.getByText('Page not found')).toBeInTheDocument();
  });

  it('renders home link', () => {
    render(<NotFoundPage />);
    expect(screen.getByText('Home')).toBeInTheDocument();
  });

  it('renders go back link', () => {
    render(<NotFoundPage />);
    expect(screen.getByText('Go back')).toBeInTheDocument();
  });
});

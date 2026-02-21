import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import ChatCorrection from '../../components/ChatCorrection';

describe('ChatCorrection', () => {
  const correction = {
    original: 'I goed home',
    corrected: 'I went home',
    explanation: 'Go is an irregular verb.',
  };

  it('renders original text', () => {
    render(<ChatCorrection correction={correction} />);
    expect(screen.getByText('I goed home')).toBeInTheDocument();
  });

  it('renders corrected text', () => {
    render(<ChatCorrection correction={correction} />);
    expect(screen.getByText('I went home')).toBeInTheDocument();
  });

  it('renders explanation', () => {
    render(<ChatCorrection correction={correction} />);
    expect(screen.getByText('Go is an irregular verb.')).toBeInTheDocument();
  });
});

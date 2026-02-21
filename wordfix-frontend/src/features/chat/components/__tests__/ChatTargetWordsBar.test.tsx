import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import ChatTargetWordsBar from '../../components/ChatTargetWordsBar';

describe('ChatTargetWordsBar', () => {
  it('renders target words', () => {
    render(<ChatTargetWordsBar words={['hello', 'world']} usedWords={['hello']} />);
    expect(screen.getByText('hello')).toBeInTheDocument();
    expect(screen.getByText('world')).toBeInTheDocument();
  });

  it('shows used/total count', () => {
    render(<ChatTargetWordsBar words={['hello', 'world', 'test']} usedWords={['hello']} />);
    expect(screen.getByText('1/3')).toBeInTheDocument();
  });

  it('returns null when no words', () => {
    const { container } = render(<ChatTargetWordsBar words={[]} usedWords={[]} />);
    expect(container.innerHTML).toBe('');
  });
});

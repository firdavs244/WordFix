import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import ChatTopicSelector from '../../components/ChatTopicSelector';

describe('ChatTopicSelector', () => {
  it('renders preset topics', () => {
    render(<ChatTopicSelector onStart={() => {}} isLoading={false} />);
    expect(screen.getByText('Travel')).toBeInTheDocument();
    expect(screen.getByText('Food')).toBeInTheDocument();
  });

  it('renders start button', () => {
    render(<ChatTopicSelector onStart={() => {}} isLoading={false} />);
    expect(screen.getByText('Start Conversation')).toBeInTheDocument();
  });

  it('shows custom topic input', () => {
    render(<ChatTopicSelector onStart={() => {}} isLoading={false} />);
    expect(screen.getByPlaceholderText(/custom topic/i)).toBeInTheDocument();
  });

  it('start button is disabled when no topic selected', () => {
    render(<ChatTopicSelector onStart={() => {}} isLoading={false} />);
    const button = screen.getByText('Start Conversation').closest('button')!;
    expect(button).toBeDisabled();
  });
});

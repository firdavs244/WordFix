import { describe, it, expect, vi } from 'vitest';
import { render, screen, userEvent } from '@/test/utils';
import AudioPlayer from '../AudioPlayer';

describe('AudioPlayer', () => {
  it('renders play button', () => {
    render(<AudioPlayer audioUrl="/audio/hello.mp3" />);
    expect(screen.getByTestId('play-button')).toBeInTheDocument();
  });

  it('has play aria-label initially', () => {
    render(<AudioPlayer audioUrl="/audio/hello.mp3" />);
    expect(screen.getByLabelText('Play')).toBeInTheDocument();
  });

  it('toggles to pause on click', async () => {
    const user = userEvent.setup();
    render(<AudioPlayer audioUrl="/audio/hello.mp3" />);
    await user.click(screen.getByTestId('play-button'));
    expect(screen.getByLabelText('Pause')).toBeInTheDocument();
  });

  it('renders replay button', () => {
    render(<AudioPlayer audioUrl="/audio/hello.mp3" />);
    expect(screen.getByTestId('replay-button')).toBeInTheDocument();
    expect(screen.getByText('Replay')).toBeInTheDocument();
  });

  it('calls onPlay when play button clicked', async () => {
    const onPlay = vi.fn();
    const user = userEvent.setup();
    render(<AudioPlayer audioUrl="/audio/hello.mp3" onPlay={onPlay} />);
    await user.click(screen.getByTestId('play-button'));
    expect(onPlay).toHaveBeenCalledTimes(1);
  });

  it('has audio-player test id', () => {
    render(<AudioPlayer audioUrl="/audio/hello.mp3" />);
    expect(screen.getByTestId('audio-player')).toBeInTheDocument();
  });

  it('calls onPlay when replay button clicked', async () => {
    const onPlay = vi.fn();
    const user = userEvent.setup();
    render(<AudioPlayer audioUrl="/audio/hello.mp3" onPlay={onPlay} />);
    await user.click(screen.getByTestId('replay-button'));
    expect(onPlay).toHaveBeenCalledTimes(1);
  });
});

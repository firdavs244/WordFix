import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@/test/utils';
import { createMockTestQuestion } from '@/test/utils';
import { fireEvent } from '@testing-library/react';
import TestSessionPage from '../../TestSessionPage';

const mockQuestions = [
  createMockTestQuestion({ id: 'q1', question_text: 'What does "hello" mean?', options: ['hola', 'mundo', 'casa', 'perro'] }),
  createMockTestQuestion({ id: 'q2', question_text: 'What does "world" mean?', options: ['mundo', 'sol', 'luna', 'mar'], order: 2 }),
];

const mockNavigate = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return { ...actual, useParams: () => ({ sessionId: 'ts-1' }), useNavigate: () => mockNavigate, useLocation: () => ({ state: { questions: mockQuestions }, pathname: '/tests/session/ts-1', search: '', hash: '', key: 'default' }) };
});

vi.mock('../TestSessionTopBar', () => ({ default: ({ current, total }: { current: number; total: number }) => <div data-testid="top-bar">Q {current + 1}/{total}</div> }));
vi.mock('@/features/review/components/SessionProgressBar', () => ({ default: () => <div data-testid="progress-bar" /> }));
vi.mock('@/features/review/components/ComboIndicator', () => ({ default: () => <div data-testid="combo" /> }));
vi.mock('@/features/review/components/XPGainPopup', () => ({ default: () => <div data-testid="xp-popup" /> }));

describe('TestSessionPage', () => {
  beforeEach(() => { mockNavigate.mockClear(); });

  it('renders the first question text', () => {
    render(<TestSessionPage />);
    expect(screen.getByText('What does "hello" mean?')).toBeInTheDocument();
  });

  it('renders the progress bar', () => {
    render(<TestSessionPage />);
    expect(screen.getByTestId('progress-bar')).toBeInTheDocument();
  });

  it('renders combo indicator', () => {
    render(<TestSessionPage />);
    expect(screen.getByTestId('combo')).toBeInTheDocument();
  });

  it('renders the top bar with current question', () => {
    render(<TestSessionPage />);
    expect(screen.getByText('Q 1/2')).toBeInTheDocument();
  });

  it('renders four options for multiple choice', () => {
    render(<TestSessionPage />);
    expect(screen.getByText('hola')).toBeInTheDocument();
    expect(screen.getByText('mundo')).toBeInTheDocument();
    expect(screen.getByText('casa')).toBeInTheDocument();
    expect(screen.getByText('perro')).toBeInTheDocument();
  });

  it('shows answer feedback after clicking an option', async () => {
    render(<TestSessionPage />);
    const option = screen.getByTestId('option-0');
    fireEvent.click(option);
    await waitFor(() => {
      expect(screen.getByText(/correct/i)).toBeInTheDocument();
    }, { timeout: 5000 });
  });
});

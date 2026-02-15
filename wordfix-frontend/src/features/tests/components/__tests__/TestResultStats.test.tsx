import { describe, it, expect } from 'vitest';
import { render, screen } from '@/test/utils';
import TestResultStats from '../TestResultStats';

describe('TestResultStats', () => {
  it('renders correct answers count', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={300} />);
    expect(screen.getByText('4')).toBeInTheDocument();
  });

  it('renders incorrect answers count', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={300} />);
    const ones = screen.getAllByText('1');
    expect(ones.length).toBeGreaterThanOrEqual(1);
  });

  it('renders total questions', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={300} />);
    expect(screen.getByText('5')).toBeInTheDocument();
  });

  it('renders formatted duration', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={125} />);
    expect(screen.getByText('2:05')).toBeInTheDocument();
  });

  it('renders all stat labels', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={300} />);
    expect(screen.getByText('Correct')).toBeInTheDocument();
    expect(screen.getByText('Incorrect')).toBeInTheDocument();
    expect(screen.getByText('Total')).toBeInTheDocument();
    expect(screen.getByText('Duration')).toBeInTheDocument();
  });

  it('has result-stats test id', () => {
    render(<TestResultStats correct={4} incorrect={1} total={5} duration={300} />);
    expect(screen.getByTestId('result-stats')).toBeInTheDocument();
  });
});

export type ImportStep = 'input' | 'review' | 'result';

export function difficultyColor(d: string): string {
  switch (d) {
    case 'easy':
      return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
    case 'medium':
      return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400';
    case 'hard':
      return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
    default:
      return '';
  }
}

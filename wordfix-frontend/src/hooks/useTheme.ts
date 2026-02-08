import { useContext } from 'react';
import { ThemeContext } from '@/providers/ThemeProvider';

/**
 * Hook to access and control the current theme.
 *
 * @returns Theme context with current theme and setter
 */
export function useTheme() {
  const context = useContext(ThemeContext);

  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }

  return context;
}

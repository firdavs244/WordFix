/**
 * Application-wide constants.
 */

export const APP_NAME = 'WordFix';
export const APP_VERSION = '1.0.0';
export const APP_DESCRIPTION = 'Master Every Word with AI-Powered Learning';

// Navigation items
export const NAV_ITEMS = [
  { label: 'Home', path: '/', icon: 'Home' },
  { label: 'Words', path: '/words', icon: 'BookOpen' },
  { label: 'Import', path: '/import', icon: 'Upload' },
  { label: 'Review', path: '/review', icon: 'Brain' },
  { label: 'Chat', path: '/chat', icon: 'MessageCircle' },
  { label: 'Tests', path: '/tests', icon: 'ClipboardCheck' },
  { label: 'Confusing Pairs', path: '/confusing-pairs', icon: 'Shuffle' },
  { label: 'Games', path: '/games', icon: 'Gamepad2' },
  { label: 'Analytics', path: '/analytics', icon: 'BarChart3' },
  { label: 'Badges', path: '/badges', icon: 'Award' },
  { label: 'Profile', path: '/profile', icon: 'User' },
] as const;

// Theme
export const THEME_STORAGE_KEY = 'wordfix-theme';

// Breakpoints
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
} as const;

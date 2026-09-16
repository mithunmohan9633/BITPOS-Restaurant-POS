/**
 * BITPOS Theme Colors
 * Extracted directly from existing web templates (login.html, pos_dashboard.html, sales_dashboard.html)
 */
export const Colors = {
  // Brand Primary & Accents
  primary: '#D38C44',
  primaryDark: '#B87533',
  primaryLight: '#F7EDE1',
  primaryFaded: 'rgba(211, 140, 68, 0.12)',

  // Surfaces & Backgrounds
  background: '#FDF8F5',
  card: '#FFFFFF',
  cardAlt: '#F9F5F1',
  border: '#E8DCCB',
  borderDark: '#D4C3AC',

  // Typography
  text: '#4A3B32',
  textSecondary: '#8A7A6F',
  textMuted: '#AFA398',
  textLight: '#FFFFFF',

  // Feedback & Status
  error: '#C96459',
  errorBg: '#FFF9F8',
  errorBorder: '#E5A59E',
  success: '#4ECB71',
  successBg: '#F0FBF3',
  warning: '#E89E38',
  info: '#4B92D4',

  // Dark Dashboard Accents (from Sales Dashboard)
  darkBg: '#1A1A2E',
  darkCard: '#16213E',
  darkBorder: '#233554',

  // Controls
  disabled: '#D8CFC8',
  disabledText: '#8E857E',
  inputBg: '#FFFFFF',
  inputFocusBorder: '#D38C44',
  shadowColor: '#4A3B32',
} as const;

export type ColorName = keyof typeof Colors;


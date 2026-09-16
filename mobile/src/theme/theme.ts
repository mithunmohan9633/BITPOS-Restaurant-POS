import { Colors } from '../constants/colors';

export const Spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 40,
} as const;

export const BorderRadius = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  full: 9999,
} as const;

export const Typography = {
  h1: {
    fontSize: 28,
    fontWeight: '800' as const,
    color: Colors.text,
    letterSpacing: -0.5,
  },
  h2: {
    fontSize: 22,
    fontWeight: '800' as const,
    color: Colors.text,
  },
  h3: {
    fontSize: 18,
    fontWeight: '700' as const,
    color: Colors.text,
  },
  subtitle: {
    fontSize: 14,
    fontWeight: '500' as const,
    color: Colors.textSecondary,
  },
  body: {
    fontSize: 15,
    fontWeight: '400' as const,
    color: Colors.text,
  },
  bodyBold: {
    fontSize: 15,
    fontWeight: '600' as const,
    color: Colors.text,
  },
  caption: {
    fontSize: 12,
    fontWeight: '500' as const,
    color: Colors.textSecondary,
  },
  button: {
    fontSize: 16,
    fontWeight: '700' as const,
    color: Colors.textLight,
  },
} as const;

export const Shadows = {
  card: {
    shadowColor: Colors.shadowColor,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.08,
    shadowRadius: 15,
    elevation: 4,
  },
  button: {
    shadowColor: Colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 3,
  },
} as const;


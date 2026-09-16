/**
 * Authentication domain types for BITPOS Mobile
 */

export type UserRole = 'admin' | 'cashier_restaurant' | 'cashier_cafe';

export interface CompanyInfo {
  id: number;
  name: string;
  pos_type: 'restaurant' | 'cafe';
  is_active: boolean;
  valid_until?: string | null;
  plan_name?: string;
  address?: string;
}

export interface UserProfile {
  id: number;
  username: string;
  email?: string;
  role: UserRole;
  is_superuser?: boolean;
  company: CompanyInfo | null;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  success: boolean;
  token: string;
  user: UserProfile;
  message?: string;
}

export interface AuthState {
  // State
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isHydrating: boolean;
  authError: string | null;
  isSubscriptionExpired: boolean;

  // Actions
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  hydrateSession: () => Promise<void>;
  setSubscriptionExpired: (expired: boolean) => void;
  clearError: () => void;
}


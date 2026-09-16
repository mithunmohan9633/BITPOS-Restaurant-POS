import { create } from 'zustand';
import { AuthState, LoginCredentials, UserProfile } from '../types/auth.types';
import { authApi } from '../services/authApi';
import {
  saveSecureToken,
  getSecureToken,
  clearSecureToken,
  saveSessionUser,
  getSessionUser,
} from '../../../services/storage/secureStorage';
import { setAuthInterceptorCallbacks } from '../../../services/api/client';

export const useAuthStore = create<AuthState>((set, get) => {
  // Wire global Axios 401 & 403 interceptors to this store
  setAuthInterceptorCallbacks({
    onUnauthorized: () => {
      get().logout();
    },
    onSubscriptionExpired: () => {
      set({ isSubscriptionExpired: true });
    },
  });

  return {
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    isHydrating: true,
    authError: null,
    isSubscriptionExpired: false,

    login: async (credentials: LoginCredentials): Promise<boolean> => {
      set({ isLoading: true, authError: null });
      try {
        const response = await authApi.login(credentials);

        // Check company subscription status (matching core.middleware.SubscriptionMiddleware)
        if (response.user.company && !response.user.company.is_active) {
          set({
            isLoading: false,
            isSubscriptionExpired: true,
            authError: 'Your subscription has expired or is deactivated. Please contact support.',
          });
          return false;
        }

        // Save credentials to secure storage
        await saveSecureToken(response.token);
        await saveSessionUser(JSON.stringify(response.user));

        set({
          user: response.user,
          token: response.token,
          isAuthenticated: true,
          isLoading: false,
          authError: null,
          isSubscriptionExpired: false,
        });

        return true;
      } catch (error: any) {
        const message = error?.message || 'Authentication failed. Please check your credentials.';
        set({
          isLoading: false,
          authError: message,
          isAuthenticated: false,
        });
        return false;
      }
    },

    logout: async (): Promise<void> => {
      set({ isLoading: true });
      try {
        await authApi.logout();
      } catch {
        // Non-blocking
      } finally {
        await clearSecureToken();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
          authError: null,
          isSubscriptionExpired: false,
        });
      }
    },

    hydrateSession: async (): Promise<void> => {
      set({ isHydrating: true });
      try {
        const token = await getSecureToken();
        const userJson = await getSessionUser();

        if (token && userJson) {
          const user: UserProfile = JSON.parse(userJson);

          // Check if subscription expired
          if (user.company && !user.company.is_active) {
            set({
              isSubscriptionExpired: true,
              isHydrating: false,
              isAuthenticated: false,
            });
            return;
          }

          set({
            token,
            user,
            isAuthenticated: true,
            isHydrating: false,
          });
          return;
        }
      } catch (error) {
        console.warn('[authStore] Session hydration failed:', error);
        await clearSecureToken();
      }

      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isHydrating: false,
      });
    },

    setSubscriptionExpired: (expired: boolean) => {
      set({ isSubscriptionExpired: expired });
    },

    clearError: () => {
      set({ authError: null });
    },
  };
});


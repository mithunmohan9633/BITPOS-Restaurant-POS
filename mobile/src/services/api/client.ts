import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { getSecureToken, clearSecureToken } from '../storage/secureStorage';

export const API_BASE_URL = process.env.API_BASE_URL || 'http://10.0.2.2:8000'; // Android emulator localhost default
export const API_BASE_URL = process.env.API_BASE_URL || 'http://192.168.1.101:8000'; // PC local Wi-Fi address

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Auth store callback delegates to avoid circular imports
type AuthCallbacks = {
  onUnauthorized?: () => void;
  onSubscriptionExpired?: () => void;
};

let authCallbacks: AuthCallbacks = {};

export const setAuthInterceptorCallbacks = (callbacks: AuthCallbacks) => {
  authCallbacks = callbacks;
};

// Request Interceptor: Attach Auth Token from Secure Storage
apiClient.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    try {
      const token = await getSecureToken();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (err) {
      console.warn('[apiClient] Error retrieving secure token for request:', err);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Global 401 & 403 handling
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token invalid or expired: clear local credentials and notify store
      await clearSecureToken();
      if (authCallbacks.onUnauthorized) {
        authCallbacks.onUnauthorized();
      }
    } else if (error.response?.status === 403) {
      // Check for subscription expiration response
      const data = error.response.data as any;
      if (data?.code === 'subscription_expired' || data?.error?.includes('subscription')) {
        if (authCallbacks.onSubscriptionExpired) {
          authCallbacks.onSubscriptionExpired();
        }
      }
    }
    return Promise.reject(error);
  }
);


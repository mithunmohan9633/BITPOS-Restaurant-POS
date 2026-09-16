/**
 * Secure Token Storage Service
 * Encapsulates encrypted credential storage for iOS (Keychain) and Android (KeyStore).
 * Provides graceful fallback for dev/testing environments.
 */

const TOKEN_KEY = 'bitpos_auth_token';
const USER_KEY = 'bitpos_user_session';

// In-memory cache for fast synchronous access
let memoryToken: string | null = null;
let memoryUser: string | null = null;

export const saveSecureToken = async (token: string): Promise<void> => {
  memoryToken = token;
  try {
    // If react-native-keychain or expo-secure-store is installed in the native environment:
    const Keychain = tryLoadKeychain();
    if (Keychain) {
      await Keychain.setGenericPassword('auth_token', token, { service: TOKEN_KEY });
      return;
    }
  } catch (err) {
    // Non-fatal, fallback to memory
    console.warn('[secureStorage] Native secure storage failed, using memory:', err);
  }
};

export const getSecureToken = async (): Promise<string | null> => {
  if (memoryToken) return memoryToken;
  try {
    const Keychain = tryLoadKeychain();
    if (Keychain) {
      const credentials = await Keychain.getGenericPassword({ service: TOKEN_KEY });
      if (credentials && credentials.password) {
        memoryToken = credentials.password;
        return credentials.password;
      }
    }
  } catch (err) {
    console.warn('[secureStorage] Error reading native token:', err);
  }
  return memoryToken;
};

export const clearSecureToken = async (): Promise<void> => {
  memoryToken = null;
  memoryUser = null;
  try {
    const Keychain = tryLoadKeychain();
    if (Keychain) {
      await Keychain.resetGenericPassword({ service: TOKEN_KEY });
    }
  } catch (err) {
    console.warn('[secureStorage] Error clearing native token:', err);
  }
};

export const saveSessionUser = async (userJson: string): Promise<void> => {
  memoryUser = userJson;
};

export const getSessionUser = async (): Promise<string | null> => {
  return memoryUser;
};

// Safe lazy loader to prevent crashing if native library is not linked in development
function tryLoadKeychain(): any {
  try {
    return require('react-native-keychain');
  } catch {
    return null;
  }
}


import React from 'react';
import { View, StyleSheet } from 'react-native';
import { useAuthStore } from '../../features/auth/store/authStore';
import { AuthNavigator } from './AuthNavigator';
import { CashierNavigator } from './CashierNavigator';
import { AdminNavigator } from './AdminNavigator';
import { Spinner } from '../../components/Loader/Spinner';
import { Colors } from '../../constants/colors';

/**
 * Master RootNavigator
 * Enforces strict role-based navigation directly mapped from core/views.py:
 * - Unauthenticated -> AuthNavigator (LoginScreen)
 * - role === 'admin' -> AdminNavigator (Sales & Analytics Dashboard)
 * - role === 'cashier_restaurant' | 'cashier_cafe' -> CashierNavigator (Restaurant POS Dashboard)
 */
export const RootNavigator: React.FC = () => {
  const { isAuthenticated, user, isHydrating, isSubscriptionExpired } = useAuthStore();

  // 1. App Startup / Session Hydration Splash
  if (isHydrating) {
    return (
      <View style={styles.loadingContainer}>
        <Spinner label="Loading BITPOS..." />
      </View>
    );
  }

  // 2. Unauthenticated or Subscription Expired State
  if (!isAuthenticated || isSubscriptionExpired || !user) {
    return <AuthNavigator />;
  }

  // 3. Role-Based Navigation Routing (Exact mirror of core/views.py login_view)
  // Store Admin: Redirect to Sales Analytics & Back-Office
  if (user.role === 'admin') {
    return <AdminNavigator />;
  }

  // Restaurant Cashier: Redirect to Frontline Dine-In POS
  if (user.role === 'cashier_restaurant' || user.role === 'cashier_cafe') {
    return <CashierNavigator />;
  }

  // Default fallback for any frontline cashier account
  return <CashierNavigator />;
};

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    backgroundColor: Colors.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
});


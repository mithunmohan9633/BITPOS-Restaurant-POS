import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuthStore } from '../../features/auth/store/authStore';
import { Button } from '../../components/Button/Button';
import { Colors } from '../../constants/colors';
import { BorderRadius, Shadows, Spacing, Typography } from '../../theme/theme';

const Stack = createNativeStackNavigator();

/**
 * Restaurant Cashier POS Dashboard Placeholder
 * Accessible only to users with role === 'cashier_restaurant'
 */
const CashierPOSPlaceholder: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Top Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.brandTitle}>BITPOS</Text>
          <Text style={styles.storeName}>{user?.company?.name || 'Restaurant POS'}</Text>
        </View>
        <TouchableOpacity
          onPress={logout}
          style={styles.logoutButton}
          activeOpacity={0.8}
        >
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      {/* Main Content */}
      <View style={styles.content}>
        <View style={styles.card}>
          <View style={styles.roleBadge}>
            <Text style={styles.roleBadgeText}>CASHIER MODE</Text>
          </View>

          <Text style={styles.cardTitle}>Restaurant POS Dashboard</Text>
          <Text style={styles.cardSubtitle}>
            Operational workspace for table management, dine-in ordering, and KOT dispatch.
          </Text>

          <View style={styles.detailsBox}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Staff User:</Text>
              <Text style={styles.detailValue}>{user?.username}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Backend Role:</Text>
              <Text style={styles.detailValueHighlight}>{user?.role}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Store Type:</Text>
              <Text style={styles.detailValue}>
                {user?.company?.pos_type === 'restaurant' ? 'Dine-In Restaurant' : 'Cafe'}
              </Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Subscription:</Text>
              <Text style={styles.detailValueSuccess}>Active</Text>
            </View>
          </View>

          <View style={styles.nextPhaseNote}>
            <Text style={styles.noteTitle}>Foundation Established ✓</Text>
            <Text style={styles.noteBody}>
              Authentication and role-based routing verified. Frontline POS ordering, tables grid,
              and KOT printing will be implemented in the next phase.
            </Text>
          </View>

          <Button
            title="Sign Out"
            onPress={logout}
            variant="secondary"
            style={styles.signOutButton}
          />
        </View>
      </View>
    </SafeAreaView>
  );
};

export const CashierNavigator: React.FC = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="POSDashboard" component={CashierPOSPlaceholder} />
    </Stack.Navigator>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: Spacing.lg,
    paddingVertical: Spacing.md,
    backgroundColor: Colors.card,
    borderBottomWidth: 1.5,
    borderBottomColor: Colors.border,
  },
  brandTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.primary,
  },
  storeName: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  logoutButton: {
    backgroundColor: Colors.errorBg,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs + 2,
    borderRadius: BorderRadius.xs,
    borderWidth: 1,
    borderColor: Colors.errorBorder,
  },
  logoutText: {
    color: Colors.error,
    fontWeight: '700',
    fontSize: 13,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.lg,
  },
  card: {
    backgroundColor: Colors.card,
    borderRadius: BorderRadius.lg,
    borderWidth: 2,
    borderColor: Colors.border,
    padding: Spacing.xl,
    width: '100%',
    maxWidth: 480,
    alignItems: 'center',
    ...Shadows.card,
  },
  roleBadge: {
    backgroundColor: Colors.primaryFaded,
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs,
    borderRadius: BorderRadius.full,
    marginBottom: Spacing.md,
  },
  roleBadgeText: {
    color: Colors.primary,
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 1,
  },
  cardTitle: {
    ...Typography.h2,
    color: Colors.text,
    textAlign: 'center',
    marginBottom: Spacing.xs,
  },
  cardSubtitle: {
    ...Typography.subtitle,
    textAlign: 'center',
    color: Colors.textSecondary,
    marginBottom: Spacing.lg,
    lineHeight: 20,
  },
  detailsBox: {
    width: '100%',
    backgroundColor: Colors.cardAlt,
    borderRadius: BorderRadius.sm,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 6,
  },
  detailLabel: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
  },
  detailValue: {
    fontSize: 14,
    color: Colors.text,
    fontWeight: '700',
  },
  detailValueHighlight: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '800',
  },
  detailValueSuccess: {
    fontSize: 14,
    color: Colors.success,
    fontWeight: '700',
  },
  nextPhaseNote: {
    backgroundColor: Colors.successBg,
    borderRadius: BorderRadius.sm,
    borderWidth: 1,
    borderColor: Colors.success,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
    width: '100%',
  },
  noteTitle: {
    fontSize: 13,
    fontWeight: '800',
    color: Colors.success,
    marginBottom: 4,
  },
  noteBody: {
    fontSize: 12,
    color: Colors.text,
    lineHeight: 18,
  },
  signOutButton: {
    width: '100%',
  },
});


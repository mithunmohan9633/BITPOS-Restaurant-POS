import React from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity } from 'react-native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useAuthStore } from '../../features/auth/store/authStore';
import { Button } from '../../components/Button/Button';
import { Colors } from '../../constants/colors';
import { BorderRadius, Shadows, Spacing, Typography } from '../../theme/theme';

const Stack = createNativeStackNavigator();

/**
 * Store Admin Sales Dashboard Placeholder
 * Accessible only to users with role === 'admin'
 */
const AdminSalesDashboardPlaceholder: React.FC = () => {
  const { user, logout } = useAuthStore();

  return (
    <SafeAreaView style={styles.safeArea}>
      {/* Top Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.brandTitle}>BITPOS</Text>
          <Text style={styles.storeName}>Store Admin • {user?.company?.name || 'Back Office'}</Text>
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
            <Text style={styles.roleBadgeText}>ADMINISTRATOR ACCESS</Text>
          </View>

          <Text style={styles.cardTitle}>Sales & Analytics Dashboard</Text>
          <Text style={styles.cardSubtitle}>
            Back-office management, daily/monthly revenue metrics, staff accounts, and report exports.
          </Text>

          <View style={styles.detailsBox}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Admin Account:</Text>
              <Text style={styles.detailValue}>{user?.username}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Backend Role:</Text>
              <Text style={styles.detailValueHighlight}>{user?.role}</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>Permissions:</Text>
              <Text style={styles.detailValue}>Full Store Management</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>POS Access:</Text>
              <Text style={styles.detailValueMuted}>Restricted (Sales & Back-Office Only)</Text>
            </View>
          </View>

          <View style={styles.nextPhaseNote}>
            <Text style={styles.noteTitle}>Foundation Established ✓</Text>
            <Text style={styles.noteBody}>
              Authentication and role-based routing verified. Executive KPI cards, 7-day revenue
              charts, and Excel/PDF report exports will be implemented in the next phase.
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

export const AdminNavigator: React.FC = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="SalesDashboard" component={AdminSalesDashboardPlaceholder} />
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
    backgroundColor: Colors.darkCard,
    borderBottomWidth: 1.5,
    borderBottomColor: Colors.darkBorder,
  },
  brandTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.primary,
  },
  storeName: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textMuted,
  },
  logoutButton: {
    backgroundColor: 'rgba(233, 69, 96, 0.15)',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs + 2,
    borderRadius: BorderRadius.xs,
    borderWidth: 1,
    borderColor: Colors.error,
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
    backgroundColor: 'rgba(99, 102, 241, 0.12)',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.xs,
    borderRadius: BorderRadius.full,
    marginBottom: Spacing.md,
  },
  roleBadgeText: {
    color: '#6366F1',
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
    color: '#6366F1',
    fontWeight: '800',
  },
  detailValueMuted: {
    fontSize: 13,
    color: Colors.textSecondary,
    fontStyle: 'italic',
  },
  nextPhaseNote: {
    backgroundColor: Colors.primaryFaded,
    borderRadius: BorderRadius.sm,
    borderWidth: 1,
    borderColor: Colors.primary,
    padding: Spacing.md,
    marginBottom: Spacing.lg,
    width: '100%',
  },
  noteTitle: {
    fontSize: 13,
    fontWeight: '800',
    color: Colors.primaryDark,
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


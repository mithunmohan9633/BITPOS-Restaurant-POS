import React from 'react';
import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import { useAuthStore } from '../store/authStore';
import { Button } from '../../../components/Button/Button';
import { Colors } from '../../../constants/colors';
import { BorderRadius, Shadows, Spacing, Typography } from '../../../theme/theme';

export const SubscriptionExpiredScreen: React.FC = () => {
  const { setSubscriptionExpired, logout } = useAuthStore();

  const handleReturnToLogin = async () => {
    setSubscriptionExpired(false);
    await logout();
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.alertIcon}>⏳</Text>
        <Text style={styles.title}>Subscription Expired</Text>
        <Text style={styles.description}>
          Your store subscription has expired or is currently inactive. Please contact your
          administrator or BITPOS support to renew your service.
        </Text>

        <View style={styles.infoBox}>
          <Text style={styles.infoText}>Support: support@bitpos.com</Text>
        </View>

        <Button
          title="Back to Login"
          onPress={handleReturnToLogin}
          variant="primary"
          style={styles.button}
        />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
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
    maxWidth: 420,
    alignItems: 'center',
    ...Shadows.card,
  },
  alertIcon: {
    fontSize: 48,
    marginBottom: Spacing.md,
  },
  title: {
    ...Typography.h2,
    color: Colors.error,
    marginBottom: Spacing.sm,
    textAlign: 'center',
  },
  description: {
    ...Typography.body,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: Spacing.lg,
  },
  infoBox: {
    backgroundColor: Colors.cardAlt,
    borderRadius: BorderRadius.sm,
    borderWidth: 1,
    borderColor: Colors.border,
    padding: Spacing.md,
    width: '100%',
    alignItems: 'center',
    marginBottom: Spacing.xl,
  },
  infoText: {
    ...Typography.caption,
    color: Colors.text,
    fontWeight: '700',
  },
  button: {
    width: '100%',
  },
});


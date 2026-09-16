import React from 'react';
import {
  View,
  Text,
  Image,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  SafeAreaView,
  useWindowDimensions,
} from 'react-native';
import { LoginForm } from '../components/LoginForm';
import { Colors } from '../../../constants/colors';
import { BorderRadius, Shadows, Spacing, Typography } from '../../../theme/theme';

export const LoginScreen: React.FC = () => {
  const { width, height } = useWindowDimensions();
  const isTablet = width >= 600;

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView
        style={styles.keyboardAvoid}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView
          contentContainerStyle={[
            styles.scrollContent,
            { minHeight: height - (Platform.OS === 'ios' ? 80 : 50) },
          ]}
          keyboardShouldPersistTaps="handled"
        >
          <View style={[styles.loginCard, isTablet && styles.tabletCard]}>
            {/* Logo & Branding Header */}
            <View style={styles.header}>
              <Image
                source={require('../../../../assets/images/logo.png')}
                style={styles.logo}
                resizeMode="contain"
              />
              <Text style={styles.tagline}>Restaurant & Cafe Point of Sale</Text>
            </View>

            {/* Login Form */}
            <LoginForm />

            {/* Card Footer */}
            <View style={styles.cardFooter}>
              <Text style={styles.footerHelp}>
                Enter your staff credentials to access your store
              </Text>
            </View>
          </View>

          {/* System Footer */}
          <View style={styles.systemFooter}>
            <Text style={styles.versionText}>BITPOS Mobile v1.0.0</Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  keyboardAvoid: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: Spacing.md,
    paddingVertical: Spacing.lg,
  },
  loginCard: {
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
  tabletCard: {
    padding: Spacing.xxl,
    maxWidth: 460,
  },
  header: {
    alignItems: 'center',
    marginBottom: Spacing.xl,
    width: '100%',
  },
  logo: {
    height: 75,
    width: 220,
    marginBottom: Spacing.sm,
  },
  tagline: {
    ...Typography.subtitle,
    color: Colors.textSecondary,
    fontWeight: '600',
    fontSize: 13,
    textAlign: 'center',
    marginTop: 2,
  },
  cardFooter: {
    marginTop: Spacing.lg,
    alignItems: 'center',
  },
  footerHelp: {
    ...Typography.caption,
    textAlign: 'center',
    color: Colors.textMuted,
    lineHeight: 18,
  },
  systemFooter: {
    marginTop: Spacing.xl,
    alignItems: 'center',
  },
  versionText: {
    ...Typography.caption,
    color: Colors.textMuted,
    fontWeight: '600',
  },
});


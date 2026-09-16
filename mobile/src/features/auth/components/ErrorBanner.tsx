import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Colors } from '../../../constants/colors';
import { BorderRadius, Spacing } from '../../../theme/theme';

interface ErrorBannerProps {
  message: string | null;
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({ message }) => {
  if (!message) return null;

  return (
    <View style={styles.banner}>
      <Text style={styles.icon}>⚠️</Text>
      <Text style={styles.text}>{message}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  banner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.errorBg,
    borderWidth: 1.5,
    borderColor: Colors.errorBorder,
    borderRadius: BorderRadius.sm,
    paddingVertical: Spacing.sm + 2,
    paddingHorizontal: Spacing.md,
    marginBottom: Spacing.md,
    width: '100%',
  },
  icon: {
    marginRight: Spacing.sm,
    fontSize: 14,
  },
  text: {
    flex: 1,
    color: Colors.error,
    fontWeight: '700',
    fontSize: 13.5,
    lineHeight: 18,
  },
});


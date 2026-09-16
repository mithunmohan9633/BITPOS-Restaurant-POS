import React from 'react';
import { View, ActivityIndicator, Text, StyleSheet } from 'react-native';
import { Colors } from '../../constants/colors';
import { Spacing } from '../../theme/theme';

interface SpinnerProps {
  label?: string;
  size?: 'small' | 'large';
  color?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  label,
  size = 'large',
  color = Colors.primary,
}) => {
  return (
    <View style={styles.container}>
      <ActivityIndicator size={size} color={color} />
      {label && <Text style={styles.label}>{label}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: Spacing.lg,
  },
  label: {
    marginTop: Spacing.sm,
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '600',
  },
});


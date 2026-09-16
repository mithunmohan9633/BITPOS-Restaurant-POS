import React from 'react';
import {
  TouchableOpacity,
  Text,
  ActivityIndicator,
  StyleSheet,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { Colors } from '../../constants/colors';
import { BorderRadius, Shadows, Spacing } from '../../theme/theme';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  loading?: boolean;
  disabled?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
  style,
  textStyle,
  fullWidth = true,
}) => {
  const isInteractive = !loading && !disabled;

  const getContainerStyle = () => {
    switch (variant) {
      case 'secondary':
        return styles.secondaryContainer;
      case 'outline':
        return styles.outlineContainer;
      case 'danger':
        return styles.dangerContainer;
      default:
        return styles.primaryContainer;
    }
  };

  const getTextStyle = () => {
    switch (variant) {
      case 'secondary':
        return styles.secondaryText;
      case 'outline':
        return styles.outlineText;
      case 'danger':
        return styles.dangerText;
      default:
        return styles.primaryText;
    }
  };

  return (
    <TouchableOpacity
      activeOpacity={0.85}
      onPress={onPress}
      disabled={!isInteractive}
      style={[
        styles.baseContainer,
        getContainerStyle(),
        fullWidth && styles.fullWidth,
        !isInteractive && styles.disabledContainer,
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator
          size="small"
          color={variant === 'outline' ? Colors.primary : Colors.textLight}
        />
      ) : (
        <Text style={[styles.baseText, getTextStyle(), textStyle]}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  baseContainer: {
    height: 52,
    borderRadius: BorderRadius.sm,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: Spacing.lg,
  },
  fullWidth: {
    width: '100%',
  },
  primaryContainer: {
    backgroundColor: Colors.primary,
    ...Shadows.button,
  },
  secondaryContainer: {
    backgroundColor: Colors.cardAlt,
    borderWidth: 1.5,
    borderColor: Colors.border,
  },
  outlineContainer: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  dangerContainer: {
    backgroundColor: Colors.error,
  },
  disabledContainer: {
    backgroundColor: Colors.disabled,
    shadowOpacity: 0,
    elevation: 0,
  },
  baseText: {
    fontSize: 16,
    fontWeight: '800',
    textAlign: 'center',
    letterSpacing: 0.2,
  },
  primaryText: {
    color: Colors.textLight,
  },
  secondaryText: {
    color: Colors.text,
  },
  outlineText: {
    color: Colors.primary,
  },
  dangerText: {
    color: Colors.textLight,
  },
});


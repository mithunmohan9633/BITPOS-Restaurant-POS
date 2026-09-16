import React, { useState } from 'react';
import {
  View,
  TextInput,
  Text,
  TouchableOpacity,
  StyleSheet,
  ViewStyle,
  TextInputProps,
} from 'react-native';
import { Colors } from '../../constants/colors';
import { BorderRadius, Spacing } from '../../theme/theme';

interface FormTextInputProps extends TextInputProps {
  label?: string;
  error?: string;
  isPassword?: boolean;
  containerStyle?: ViewStyle;
}

export const FormTextInput = React.forwardRef<TextInput, FormTextInputProps>(
  (
    {
      label,
      error,
      isPassword = false,
      containerStyle,
      style,
      ...props
    },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false);
    const [isPasswordVisible, setIsPasswordVisible] = useState(false);

    const hasError = Boolean(error);

    return (
      <View style={[styles.container, containerStyle]}>
        {label && <Text style={styles.label}>{label}</Text>}

        <View
          style={[
            styles.inputWrapper,
            isFocused && styles.inputWrapperFocused,
            hasError && styles.inputWrapperError,
          ]}
        >
          <TextInput
            ref={ref}
            style={[styles.input, style]}
          placeholderTextColor={Colors.textMuted}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          secureTextEntry={isPassword && !isPasswordVisible}
          autoCapitalize="none"
          autoCorrect={false}
          {...props}
        />

        {isPassword && (
          <TouchableOpacity
            style={styles.toggleButton}
            onPress={() => setIsPasswordVisible((prev) => !prev)}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
            accessibilityLabel={isPasswordVisible ? 'Hide password' : 'Show password'}
          >
            <Text style={styles.toggleText}>
              {isPasswordVisible ? 'Hide' : 'Show'}
            </Text>
          </TouchableOpacity>
        )}
      </View>

      {hasError && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
});

FormTextInput.displayName = 'FormTextInput';

const styles = StyleSheet.create({
  container: {
    marginBottom: Spacing.md,
    width: '100%',
  },
  label: {
    fontSize: 14,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: Spacing.xs,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.inputBg,
    borderWidth: 2,
    borderColor: Colors.border,
    borderRadius: BorderRadius.sm,
    height: 52,
    paddingHorizontal: Spacing.md,
  },
  inputWrapperFocused: {
    borderColor: Colors.primary,
  },
  inputWrapperError: {
    borderColor: Colors.error,
    backgroundColor: Colors.errorBg,
  },
  input: {
    flex: 1,
    height: '100%',
    color: Colors.text,
    fontSize: 16,
    fontWeight: '500',
    paddingVertical: 0,
  },
  toggleButton: {
    paddingLeft: Spacing.sm,
    justifyContent: 'center',
  },
  toggleText: {
    color: Colors.primary,
    fontWeight: '700',
    fontSize: 14,
  },
  errorText: {
    color: Colors.error,
    fontSize: 13,
    fontWeight: '600',
    marginTop: 4,
    marginLeft: 2,
  },
});

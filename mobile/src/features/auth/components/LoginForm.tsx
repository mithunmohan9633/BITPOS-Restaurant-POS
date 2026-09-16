import React, { useRef } from 'react';
import { View, StyleSheet, TextInput } from 'react-native';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { loginSchema, LoginFormData } from '../validation/authValidation';
import { useAuthStore } from '../store/authStore';
import { FormTextInput } from '../../../components/Input/FormTextInput';
import { Button } from '../../../components/Button/Button';
import { ErrorBanner } from './ErrorBanner';
import { Spacing } from '../../../theme/theme';

export const LoginForm: React.FC = () => {
  const { login, isLoading, authError, clearError } = useAuthStore();
  const passwordInputRef = useRef<TextInput>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
    },
    mode: 'onBlur',
  });

  const onSubmit = async (data: LoginFormData) => {
    clearError();
    await login(data);
  };

  return (
    <View style={styles.container}>
      {/* Backend / Global Auth Error Banner */}
      <ErrorBanner message={authError} />

      {/* Username Field */}
      <Controller
        control={control}
        name="username"
        render={({ field: { onChange, onBlur, value } }) => (
          <FormTextInput
            label="Username"
            placeholder="e.g. sultan1 or city"
            value={value}
            onChangeText={(text) => {
              if (authError) clearError();
              onChange(text.toLowerCase().trim());
            }}
            onBlur={onBlur}
            error={errors.username?.message}
            autoCapitalize="none"
            autoCorrect={false}
            returnKeyType="next"
            onSubmitEditing={() => passwordInputRef.current?.focus()}
            editable={!isLoading}
          />
        )}
      />

      {/* Password Field */}
      <Controller
        control={control}
        name="password"
        render={({ field: { onChange, onBlur, value } }) => (
          <FormTextInput
            ref={passwordInputRef as any}
            label="Password"
            placeholder="Enter your password"
            value={value}
            onChangeText={(text) => {
              if (authError) clearError();
              onChange(text);
            }}
            onBlur={onBlur}
            error={errors.password?.message}
            isPassword
            returnKeyType="done"
            onSubmitEditing={handleSubmit(onSubmit)}
            editable={!isLoading}
          />
        )}
      />

      {/* Submit Button */}
      <Button
        title="Sign In"
        onPress={handleSubmit(onSubmit)}
        loading={isLoading}
        style={styles.submitButton}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  submitButton: {
    marginTop: Spacing.sm,
  },
});


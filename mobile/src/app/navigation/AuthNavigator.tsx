import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { AuthStackParamList } from './types';
import { LoginScreen } from '../../features/auth/screens/LoginScreen';
import { SubscriptionExpiredScreen } from '../../features/auth/screens/SubscriptionExpiredScreen';

const Stack = createNativeStackNavigator<AuthStackParamList>();

export const AuthNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        animation: 'fade',
      }}
    >
      <Stack.Screen name="Login" component={LoginScreen} />
      <Stack.Screen name="SubscriptionExpired" component={SubscriptionExpiredScreen} />
    </Stack.Navigator>
  );
};


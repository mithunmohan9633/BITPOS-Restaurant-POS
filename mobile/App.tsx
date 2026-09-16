import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { AppProvider } from './src/app/providers/AppProvider';
import { RootNavigator } from './src/app/navigation/RootNavigator';
import { useAuthStore } from './src/features/auth/store/authStore';

export default function App() {
  const hydrateSession = useAuthStore((state) => state.hydrateSession);

  useEffect(() => {
    // Hydrate token and session on application startup
    hydrateSession();
  }, [hydrateSession]);

  return (
    <AppProvider>
      <NavigationContainer>
        <RootNavigator />
      </NavigationContainer>
    </AppProvider>
  );
}


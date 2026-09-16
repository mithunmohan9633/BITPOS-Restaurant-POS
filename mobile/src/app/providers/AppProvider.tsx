import React from 'react';
import { StatusBar } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Colors } from '../../constants/colors';

interface AppProviderProps {
  children: React.ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  return (
    <SafeAreaProvider>
      <StatusBar
        barStyle="dark-content"
        backgroundColor={Colors.background}
      />
      {children}
    </SafeAreaProvider>
  );
};


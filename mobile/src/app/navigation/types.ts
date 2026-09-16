import { NavigatorScreenParams } from '@react-navigation/native';

export type AuthStackParamList = {
  Login: undefined;
  SubscriptionExpired: undefined;
};

export type CashierTabParamList = {
  POSDashboard: undefined;
  Tables: undefined;
  ActiveOrders: undefined;
  Profile: undefined;
};

export type AdminTabParamList = {
  SalesDashboard: undefined;
  OrderHistory: undefined;
  Expenses: undefined;
  Settings: undefined;
};

export type RootStackParamList = {
  Auth: NavigatorScreenParams<AuthStackParamList>;
  Cashier: NavigatorScreenParams<CashierTabParamList>;
  Admin: NavigatorScreenParams<AdminTabParamList>;
};


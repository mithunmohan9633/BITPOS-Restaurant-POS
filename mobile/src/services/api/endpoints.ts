/**
 * Centralized API endpoints for BITPOS backend
 */
export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/api/auth/login/',
  ME: '/api/auth/me/',
  LOGOUT: '/api/auth/logout/',

  // Core POS
  COMPANIES: '/api/companies/',
  USERS: '/api/users/',
  MENU: '/api/menu/',
  CREATE_ORDER: '/api/create-order/',
  ACTIVE_ORDERS: '/api/active-orders/',
  TABLE_ORDERS: (tableId: number) => `/api/table-orders/${tableId}/`,
  PAY_ORDER: (orderNumber: string) => `/api/pay-order/${orderNumber}/`,
  TRANSFER_TABLE: '/api/transfer-table/',
  INVOICE_ORDER: (orderNumber: string) => `/api/invoice-order/${orderNumber}/`,

  // Hardware Diagnostics & Reprinting
  TEST_PRINTER: (printerId: number) => `/api/printers/test/${printerId}/`,
  PRINT_KOT: (orderNumber: string) => `/api/print/kot/${orderNumber}/`,
  PRINT_BILL: (orderNumber: string) => `/api/print/bill/${orderNumber}/`,
} as const;


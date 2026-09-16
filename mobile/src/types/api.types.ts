export interface ApiResponse<T = any> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
  code?: string;
}

export interface ApiErrorResponse {
  error: string;
  code?: string;
  details?: Record<string, string[]>;
}


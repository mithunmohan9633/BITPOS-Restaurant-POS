import { z } from 'zod';

/**
 * Zod validation schema matching existing BITPOS frontend & backend validation logic.
 * Source: validate_credentials() in core/views.py
 */
export const loginSchema = z.object({
  username: z
    .string()
    .min(1, 'Username is required')
    .regex(/^[a-z0-9]+$/, 'Username must be alphanumeric and lowercase only'),
  password: z
    .string()
    .min(1, 'Password is required'),
});

export type LoginFormData = z.infer<typeof loginSchema>;


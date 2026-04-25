import { z } from "zod";

// Validates score form input before API submission.
export const healthInputSchema = z.object({
  passwordCount: z
    .number({ invalid_type_error: "Please enter a valid number." })
    .int("Please enter a whole number.")
    .min(0, "Password count cannot be negative.")
    .max(1_000_000, "Password count is too large."),
  oldestPasswordAgeDays: z
    .number({ invalid_type_error: "Please enter a valid number." })
    .int("Please enter a whole number.")
    .min(0, "Oldest password age cannot be negative.")
    .max(36_500, "Oldest password age is too large."),
});

export type HealthInput = z.infer<typeof healthInputSchema>;

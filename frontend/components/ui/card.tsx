import * as React from "react";
import { cn } from "@/lib/utils";

// Provides a shadcn-style card container used for score visualization.
export const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("rounded-xl border bg-white text-slate-900 shadow-sm", className)}
      {...props}
    />
  ),
);
Card.displayName = "Card";

// Renders card section wrapper for spacing and grouping.
export const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6", className)} {...props} />
));
CardContent.displayName = "CardContent";

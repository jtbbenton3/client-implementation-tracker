// frontend/src/components/ui/card.jsx
import React from "react";

export function Card({ children, className = "", ...props }) {
  return (
    <div
      className={`border rounded-lg shadow-sm bg-white ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardContent({ children, className = "", ...props }) {
  return (
    <div className={`p-4 ${className}`} {...props}>
      {children}
    </div>
  );
}
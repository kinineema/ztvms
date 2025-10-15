import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import AppShell from "./components/AppShell";
import ScanPage from "./pages/ScanPage";
import Login from "./features/auth/login"; // note: capital L (match file case)
import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      {/* Public route */}
      <Route path="/login" element={<Login />} />

      {/* Protected area */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppShell>
              <ScanPage />
            </AppShell>
          </ProtectedRoute>
        }
      />

      {/* Catch-all redirect */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

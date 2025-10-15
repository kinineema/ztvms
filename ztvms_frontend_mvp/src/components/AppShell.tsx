import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Button,
} from "@mui/material";
import { useAuth } from "../features/auth/AuthContext";

export default function AppShell({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();

  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default" }}>
      <AppBar
        position="sticky"
        elevation={0}
        sx={{
          background: "rgba(17,24,39,0.7)", // translucent dark glass
          backdropFilter: "blur(8px) saturate(120%)",
          borderBottom: "1px solid rgba(255,255,255,0.08)",
        }}
      >
        <Toolbar sx={{ display: "flex", alignItems: "center", gap: 2 }}>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              letterSpacing: 0.5,
              flexGrow: 1,
              color: "text.primary",
            }}
          >
            🔒 ZTVMS | SecScan
          </Typography>

          {user && (
            <Box display="flex" alignItems="center" gap={2}>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                {user.email} — <strong>{user.role}</strong>
              </Typography>
              <Button
                color="secondary"
                variant="outlined"
                size="small"
                onClick={logout}
                sx={{
                  borderColor: "rgba(255,255,255,0.25)",
                  "&:hover": { borderColor: "secondary.main" },
                }}
              >
                Logout
              </Button>
            </Box>
          )}
        </Toolbar>
      </AppBar>

      <Container
        maxWidth="lg"
        sx={{
          mt: 4,
          mb: 6,
          color: "text.primary",
        }}
      >
        {children}
      </Container>
    </Box>
  );
}

import React, { useState } from "react";
import { Box, Paper, TextField, Button, Typography, Alert } from "@mui/material";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    try {
      await login(email, pw);
      nav("/", { replace: true });
    } catch (e: any) {
      setErr(e?.response?.data?.detail || "Login failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <Box display="flex" justifyContent="center" mt={8}>
      <Paper sx={{ p: 3, width: 420 }}>
        <Typography variant="h6" gutterBottom>Sign in</Typography>
        <form onSubmit={submit}>
          <TextField label="Email" fullWidth margin="normal" value={email} onChange={e=>setEmail(e.target.value)} />
          <TextField label="Password" type="password" fullWidth margin="normal" value={pw} onChange={e=>setPw(e.target.value)} />
          {err && <Alert severity="error" sx={{ mt: 1 }}>{err}</Alert>}
          <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }} disabled={busy}>
            {busy ? "Signing in..." : "Sign in"}
          </Button>
          <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>
            Demo users: <b>admin@demo/admin</b>, <b>analyst@demo/analyst</b>, <b>viewer@demo/viewer</b>
          </Typography>
        </form>
      </Paper>
    </Box>
  );
}

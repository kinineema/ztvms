import React, { useState } from "react";
import { Box, Paper, TextField, Button, Typography, Alert } from "@mui/material";
import { useAuth } from "./AuthContext";
import { useNavigate } from "react-router-dom";

async function login(email: string, password: string) {
// REAL backend call (FastAPI + OAuth2 form fields)
const form = new URLSearchParams();
form.set("username", email);
form.set("password", password);

const res = await api.post<{ access_token: string; refresh_token: string; role: "admin"|"analyst"|"viewer" }>(
  "/auth/login",
  form,
  { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
);

const { access_token, role } = res.data;
const u: User = { email, role };
localStorage.setItem("token", access_token);
localStorage.setItem("user", JSON.stringify(u));
setToken(access_token);
setUser(u);
}

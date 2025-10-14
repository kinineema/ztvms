# ZTVMS Frontend MVP (React + Vite + TS + MUI)

This is the minimal frontend to satisfy the MVP checklist:
- Target URL input
- Start scan (POST /scans)
- Show scan ID and status (GET /scans/{id}/status) with polling
- View Findings (GET /scans/{id}/report) raw JSON

## Prereqs
- Node 18+
- Backend running at http://localhost:8000 with routes:
  - POST /scans
  - GET  /scans/{id}/status
  - GET  /scans/{id}/report

## Run
```bash
npm install
npm run dev
```

The Vite dev server proxies `/scans` to `http://localhost:8000`.
Edit `vite.config.ts` if your API is elsewhere.

=====================================================================================
Flow:
Frontend (React)
   ↓
Login (/auth/login) → JWTs
   ↓
All API calls attach "Authorization: Bearer <token>"
   ↓
FastAPI verifies token via get_current_user()
   ↓
  ├─ /scans         (admins/analysts only)
  ├─ /reports       (viewers allowed)
  ├─ /threat-model  (protected)
  └─ /dashboard     (role-based access)
=====================================================================================
PROJECT Progress Notes:

Backend Integration --> Pending
Frontend --> For now we use MOCK env
  Later remove and connect to proxy
  Authentication/Login part uses JWT Token system for easy integration and easier for API calls --> Currently uses MOCK env, later switched to JWT once backend integrated

Why JWT:
  Proves the user’s identity to every API request without needing a session.
  Protects API calls between frontend and backend
  Prevents unauthorized or cross-site misuse of your vulnerability platform.
With JWT:
  Only authenticated users can access scanning or reports.
  Every request is cryptographically verified.
  You can control permissions by role.
  This satisfies both the Confidentiality and Integrity aspects of the CIA triad your synopsis mentions.

Commands to run application
FRONTEND Window
npm install
npm i react-router-dom
npm run dev

BACKEND WINDOW
uvicorn app.main:app --reload
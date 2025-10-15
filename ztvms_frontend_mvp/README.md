# ZTVMS Frontend (React + Vite + TS + MUI)
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
Frontend --> For now we use MOCK env //MOCK removed and integrated with backend
API --> To check API: http://127.0.0.1:8000/docs#/
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

GIT COMMIT
  git init
  git add .
  git commit -m "Initial complete MVP: frontend + backend + dark theme + MTM"
  git branch -M main
  git push -u origin main

//While making changes:
  git add .
  git commit -m "Added database integration and improved login"
  git push


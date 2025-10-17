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




Component

🧑 User Access

User → React Frontend

No user is trusted by default. Every login attempt must be authenticated using valid credentials.

JWT Authentication via FastAPI

💻 Frontend Layer

React + Vite + MUI

No direct data access; communicates only via API calls over HTTPS. Stores tokens securely in browser.

Axios interceptor with JWT; localStorage or secure cookies

🌐 API Gateway

FastAPI

Each request is verified using the JWT. Role-based access (Admin/Analyst/Viewer) controls what each user can do.

FastAPI + PyJWT middleware + Pydantic validation

⚙️ Backend Core

FastAPI Services (Auth, Scans, Reports)

Acts as central gatekeeper; enforces Zero-Trust for all incoming traffic, sanitizes input, and logs all actions.

FastAPI, SQLAlchemy ORM

🧰 Vulnerability Scanning Service

OWASP ZAP (Dynamic Analysis)

Scans user-provided target URLs for live vulnerabilities (SQL injection, XSS, CSRF, etc.).

OWASP ZAP API

💾 Database Layer

PostgreSQL

Stores users, scans, findings. Access restricted to FastAPI only. No direct external queries allowed.

PostgreSQL with strict role-based privileges

🧠 Threat Modeling

Microsoft Threat Modeling Tool

Models system architecture and threats based on CIA/STRIDE; guides what to test and protect.

Microsoft TMT

🧑‍💻 Code Security (SAST)

Bandit

Analyzes Python backend code for unsafe functions, weak cryptography, and security misconfigurations.

Bandit

🧩 Dependency Security (SCA)

Safety / npm audit

Checks backend (Python) and frontend (React) dependencies for known CVEs.

Safety, npm audit

🔄 CI/CD or Dev Pipeline

Git + GitHub Actions

Runs Bandit and Safety automatically before deployment to prevent insecure code merges.

GitHub Actions, Bandit, Safety

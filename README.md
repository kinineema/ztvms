
Create **top-level README.md** (in the ztvms root):

```md
# ZTVMS – Zero-Trust Vulnerability Management (MVP)

Monorepo with:
- `frontend/` React app (login + scan UI)
- `backend/` FastAPI API (JWT auth + minimal scans)

## Quickstart

### Backend
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

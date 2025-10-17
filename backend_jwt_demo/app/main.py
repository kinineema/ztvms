from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .deps import get_current_user
from .scans import router as scans_router   # note the dot (relative) here too
from .zap_service import zap

app = FastAPI(title="SecScan API (Auth)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(scans_router) 

@app.get("/zap/health")
def zap_health():
    # This will raise if ZAP is unreachable or API key is wrong
    return {"version": zap.core.version}

@app.get("/me")
def me(user = Depends(get_current_user)):
    return user

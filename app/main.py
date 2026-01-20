# app/main.py

from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.core import create_jwt

# Inicializa a API
app = FastAPI(title="FreeFire JWT API", version="1.0.0")

# --- CONFIGURAÇÃO DE CORS (ESSENCIAL) ---
# Isso libera o acesso para que seu site consiga pedir o token à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite pedidos de qualquer lugar (Netlify, Localhost, etc)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

class TokenRequest(BaseModel):
    uid: str
    password: str

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "JWT API running. Use POST /api/token or GET /api/token?uid=...&password=...",
    }

@app.get("/api/token")
async def get_token(uid: str = Query(...), password: str = Query(...)):
    """Gera o token via método GET"""
    try:
        result = await create_jwt(uid, password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/token")
async def post_token(payload: TokenRequest = Body(...)):
    """Gera o token via método POST"""
    try:
        result = await create_jwt(payload.uid, payload.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
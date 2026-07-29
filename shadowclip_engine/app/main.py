from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routers import auth as auth_router
from app.routers import admin as admin_router


app = FastAPI(title="ShadowClip API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/hello")
def hello():
    return {"message": "Hola, ShadowClip está vivo ✨"}

# Tu endpoint de ejemplo:
# @app.post("/add_link") ...

# Rutas nuevas
app.include_router(auth_router.router)
app.include_router(admin_router.router)

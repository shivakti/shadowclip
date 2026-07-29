from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Models ---
class User(BaseModel):
    email: str
    password: str

# --- Mock Database ---
users_db = {}

# --- Routes ---
@app.get("/")
def home():
    return {"message": "Welcome to ShadowClip Backend"}

@app.post("/register")
def register(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = user.password
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    if user.email not in users_db or users_db[user.email] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

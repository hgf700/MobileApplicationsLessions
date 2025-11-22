from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount statycznych plików pod /static
app.mount("/static", StaticFiles(directory="www"), name="static")

# Model logowania
class Authorize(BaseModel):
    email: str
    password: str

# Endpoint logowania
@app.post("/app/login")
def login(action: Authorize):
    if action.email == "123" and action.password == "123":
        return {"success": True, "message": "Zalogowano!"}
    return {"success": False, "message": "Nieprawidłowy login"}

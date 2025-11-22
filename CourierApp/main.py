from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    message: str

@app.post("/action")
def do_action(action: Action):
    print("ODEBRANO:", action.message)
    return {"status": "ok", "received": action.message}

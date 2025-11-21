from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

app = FastAPI()

class User(BaseModel):
    id: int | None = None
    name: str
    email: str

# Prosta baza w pamięci
users = [
    {"id": 1, "name": "Jan", "email": "jan@example.com"},
    {"id": 2, "name": "Anna", "email": "anna@example.com"}
]

# GET – pobierz wszystkich
@app.get("/users")
def get_users():
    return users

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# GET – pobierz jednego
@app.get("/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u["id"] == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

# POST – dodaj użytkownika
@app.post("/users")
def create_user(user: User):
    new_id = max(u["id"] for u in users) + 1
    new_user = {"id": new_id, "name": user.name, "email": user.email}
    users.append(new_user)
    return new_user

# PUT – aktualizuj użytkownika
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    for u in users:
        if u["id"] == user_id:
            u["name"] = updated_user.name
            u["email"] = updated_user.email
            return u
    raise HTTPException(status_code=404, detail="User not found")

# DELETE – usuń użytkownika
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users
    filtered = [u for u in users if u["id"] != user_id]
    if len(filtered) == len(users):
        raise HTTPException(status_code=404, detail="User not found")
    users = filtered
    return {"message": "User deleted"}

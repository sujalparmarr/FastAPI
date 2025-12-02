from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import json 

app = FastAPI()

class User(BaseModel):
    name: str = Field(..., min_length=3)   
    email: str                             
    age: Optional[int] = None            
    skills: List[str] = []               
    active: bool = True
    
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

@app.post("/register")
def register_user(user: User):
    users = load_users()
    users.append(user.dict())
    save_users(users)

    return {"message": "User registered successfully!", "data": user}

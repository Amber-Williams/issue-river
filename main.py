from uuid import UUID, uuid4
from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    contributor	 = "contributor"

class User(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: Role

class Company(BaseModel):
    name: str
    industry: str
    number_employees: int

app = FastAPI()

@app.get("/user")
async def read_user(user_id: str):
    return {"user_id": user_id}

@app.post("/user")
async def create_user(user: User):
    id: UUID = str(uuid4())
    return {"id": id, **user.dict()}

@app.delete("/user")
async def delete_user(user_id: UUID):
    return {}

@app.get("/company")
async def read_company(company_id: str):
    return {"company_id": company_id}

@app.post("/company")
async def create_company(company: Company):
    id: UUID = str(uuid4())
    return {"id": id, **company.dict()}

@app.delete("/company")
async def delete_company(company_id: UUID):
    return {}
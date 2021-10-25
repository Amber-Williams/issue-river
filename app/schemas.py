from typing import List, Optional
from enum import Enum

from pydantic import BaseModel

class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    contributor	 = "contributor"

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: Optional[Role]
    workspace: Optional[int]

    class Config:
        # set to include relationship data
        orm_mode = True

class WorkspaceCreate(BaseModel):
    name: str
    user_id: int

class WorkspaceEdit(BaseModel):
    id: int
    user_id: int

class Workspace(BaseModel):
    id: int
    name: str
    users: List[User] = []

    class Config:
        # set to include relationship data
        orm_mode = True

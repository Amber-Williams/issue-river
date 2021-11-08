from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field

class Role(str, Enum):
    owner = "owner"
    admin = "admin"
    contributor	 = "contributor"

class UserBase(BaseModel):
    email: str = Field(..., max_length=255)
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., max_length=128)

class User(UserBase):
    id: int
    is_active: bool
    role: Optional[Role]
    workspace: Optional[int]

    class Config:
        # set to include relationship data
        orm_mode = True

class WorkspaceCreate(BaseModel):
    name: str = Field(..., max_length=128)
    user_id: int

class WorkspaceEdit(BaseModel):
    id: int
    user_id: int

class WorkspaceEditRole(WorkspaceEdit):
    role: Role


class Workspace(BaseModel):
    id: int
    name: str
    users: List[User] = []

    class Config:
        # set to include relationship data
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
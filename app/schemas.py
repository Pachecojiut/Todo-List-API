from pydantic import BaseModel, Field, EmailStr
from typing import Literal

class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str

#! criando os moldes de dados

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: Literal['todo', 'in_progress', 'done'] = 'todo'

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str


class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    page: int
    limit: int
    total: int

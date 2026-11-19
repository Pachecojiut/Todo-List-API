from pydantic import BaseModel, Field, EmailStr

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

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None

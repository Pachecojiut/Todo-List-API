from pydantic import BaseModel, Field, EmailStr, StringConstraints, field_validator
from typing import Literal, Annotated

#?remove espaços nas pontas e exige pelo menos 1 caractere visível
TextoCurto = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]

def _senha_cabe_no_bcrypt(senha: str) -> str:
    #! O bcrypt só aceita até 72 BYTES (acentos e emojis ocupam mais de 1 byte)
    if len(senha.encode('utf-8')) > 72:
        raise ValueError('A senha deve ter no máximo 72 bytes (acentos e emojis ocupam mais de 1 byte)')
    return senha


class UserRegister(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)

    @field_validator('password')
    @classmethod
    def validar_senha(cls, valor: str) -> str:
        return _senha_cabe_no_bcrypt(valor)

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

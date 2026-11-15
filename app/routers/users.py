from fastapi import APIRouter
from app.schemas import UserRegister

rota = APIRouter()

@rota.post('/register')
def user_registro(dados: UserRegister):
    return {'message': 'Usuário Criado'}


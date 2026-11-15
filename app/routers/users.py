from fastapi import APIRouter, HTTPException
from app.schemas import UserRegister
from app.database import get_connection

rota = APIRouter()

@rota.post('/register')
def user_registro(dados: UserRegister):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM produtos WHERE nome = %s", (dados.email,))
        usuario = cursor.fetchone()
        if usuario:
            raise HTTPException(status_code=409, detail='E-mail já cadastrado')
        return {'message': 'Usuário Criado'}
    finally:
        conexao.close()


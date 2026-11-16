from fastapi import APIRouter, HTTPException
from app.schemas import UserRegister
from app.database import get_connection
from app.security import hash_password

rota = APIRouter()

@rota.post('/register')
def user_registro(dados: UserRegister):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", (dados.email,))
        usuario = cursor.fetchone()
        if usuario:
            raise HTTPException(status_code=409, detail='E-mail já cadastrado')
        senha_hash = hash_password(dados.password)
        cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)', (dados.name, dados.email, senha_hash))
        conexao.commit()
        return {'message': 'Usuário Criado'}
    finally:
        conexao.close()


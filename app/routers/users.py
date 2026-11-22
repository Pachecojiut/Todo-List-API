from fastapi import APIRouter, HTTPException
from app.schemas import TokenResponse, UserRegister, UserLogin
from app.database import get_connection
from app.security import hash_password, create_token, verify_password

rota = APIRouter()

@rota.post('/register', status_code=201, response_model=TokenResponse, summary="Register a new user", tags=["Auth"])
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
        id_user = cursor.lastrowid
        token = create_token(id_user)
        conexao.commit()
        return {'token': token}
    finally:
        conexao.close()

@rota.post('/login', response_model=TokenResponse, summary="Log in and get a token", tags=["Auth"])
def user_login(dados: UserLogin):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE email = %s', (dados.email,))
        usuario = cursor.fetchone()
        if not usuario or not verify_password(dados.password, usuario['password_hash']):
            raise HTTPException(status_code=401, detail='E-mail ou senha inválidos')
        token = create_token(usuario['id'])
        return {'token': token}
    finally:
        conexao.close()


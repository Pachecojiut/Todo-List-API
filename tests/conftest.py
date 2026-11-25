import os 

os.environ['DB_NAME'] = 'todo_test'
os.environ['SECRET_KEY'] = 'chave_de_acesso_para_os_testes_com_mais_de_32_caracteres'

import pytest
from fastapi.testclient import TestClient
from app.database import get_connection
from app.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def limpar_banco():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT DATABASE() AS banco')
        banco = cursor.fetchone()['banco']
        if banco != 'todo_test':
            raise RuntimeError(f'Banco incorreto: {banco!r}.' " A fixture só pode limpar o banco 'todo_test'.")

        cursor.execute('DELETE FROM todos')
        cursor.execute('DELETE FROM users')
        connection.commit()
        cursor.close()
    finally:
        connection.close()

@pytest.fixture
def auth_headers():
    resposta = client.post('/register', json={
        'name': 'Ellen Ferreira',
        'email': 'ellen@ferreira.com',
        'password': 'ferreira123'
    })

    assert resposta.status_code == 201, (
        f"Erro ao cadastrar usuário: {resposta.json()}")

    token = resposta.json()['token']

    return {'Authorization': f'Bearer {token}'}

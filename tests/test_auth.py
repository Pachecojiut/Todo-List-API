from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_cadastro_com_sucesso():
    resposta = client.post('/register', json={
        'name': 'John Doe',
        'email': 'john@doe.com',
        'password': 'password123',
    })
    assert resposta.status_code == 201
    assert 'token' in resposta.json()

def test_email_repetido():
    resposta_1 = client.post('/register', json={
        'name': 'Maria Luiza',
        'email': 'Luiza@Maria.com',
        'password': 'password1234',
    })
    resposta_2 = client.post('/register', json={
        'name': 'Maria Luiza',
        'email': 'Luiza@Maria.com',
        'password': 'password1234',
    })
    assert resposta_1.status_code == 201
    assert resposta_2.status_code == 409

def test_login_correto():
    resposta_cad = client.post('/register', json={
        'name': 'Ellen Ferreira',
        'email': 'ellen@ferreira.com',
        'password': 'ferreira123',
    })
    assert resposta_cad.status_code == 201

    resposta_login = client.post('/login', json={
        'email': 'ellen@ferreira.com',
        'password': 'ferreira123',
    })
    assert resposta_login.status_code == 200
    assert 'token' in resposta_login.json()

def test_login_senha_errada():
    resposta_cad = client.post('/register', json={
        'name': 'Elizabeth',
        'email': 'eliza@beth.com',
        'password': 'elizabeth123',
    })
    assert resposta_cad.status_code == 201
    resposta_login = client.post('/login', json={
        'email': 'eliza@beth.com',
        'password': 'elizabeth1234',
    })
    assert resposta_login.status_code == 401
    



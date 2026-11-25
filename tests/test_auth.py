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

#!

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

#!

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

#!

def test_login_email_inexistente():
    resposta_cad = client.post('/register', json={
        'name': 'Lunna',
        'email': 'lunna@nascimento.com',
        'password': 'lunninha16',
    })
    assert resposta_cad.status_code == 201

    reposta_login_senha_errada = client.post('/login',json={
    'email': 'lunna@nascimento.com',
    'password': 'luninha15',
    })
    assert reposta_login_senha_errada.status_code == 401

    resposta_login_email_inexistente = client.post('/login',json={
    'email': 'billy@bruto.com',
    'password': 'maviedelicia066'
    })
    assert resposta_login_email_inexistente.status_code == 401

    mensagem_senha_errada = reposta_login_senha_errada.json()['detail']
    mensagem_email_inexistente = resposta_login_email_inexistente.json()['detail']

    assert mensagem_senha_errada == mensagem_email_inexistente
    assert mensagem_senha_errada == 'E-mail ou senha inválidos'

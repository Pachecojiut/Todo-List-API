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

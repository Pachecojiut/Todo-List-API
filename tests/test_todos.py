from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_tarefa(auth_headers):
    resposta = client.post('/todos', json={
        'title': 'Estudar',
        'description': 'Linguagem GO',
        'status': 'todo',
    }, headers=auth_headers )
    assert resposta.status_code == 201

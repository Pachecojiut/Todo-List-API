from fastapi.testclient import TestClient
from app.main import app

client = TestClient (app)

def test_docs_abre():
    resposta = client.get('/docs')
    assert resposta.status_code == 200






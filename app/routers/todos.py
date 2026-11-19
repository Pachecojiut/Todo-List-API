from fastapi import APIRouter, Depends
from app.schemas import TodoCreate, TodoResponse
from app.database import get_connection
from app.dependencies import get_current_user_id

rota = APIRouter()

@rota.post('/todos', status_code=201, response_model=TodoResponse)
def criar_todo(
    dados: TodoCreate,
    user_id: int = Depends(get_current_user_id)
):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO todos (user_id, title, description) VALUES (%s, %s, %s)', (user_id, dados.title, dados.description))
        todo_id = cursor.lastrowid
        conexao.commit()
        return {'id': todo_id,
                'title': dados.title,
                'description': dados.description}
    finally:
        conexao.close()

from fastapi import APIRouter, Depends, Query, HTTPException
from app.schemas import TodoCreate, TodoResponse, TodoListResponse
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

@rota.get('/todos', response_model=TodoListResponse)
def listar_todos(
    page: int = Query(1, ge=1),
    limit: int= Query(10, ge=1, le=100),
    user_id: int= Depends(get_current_user_id)
):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        offset = (page - 1) * limit
        cursor.execute('SELECT id, title, description FROM todos WHERE user_id = %s ORDER BY id LIMIT %s OFFSET %s', (user_id, limit, offset),)
        todos = cursor.fetchall()
        cursor.execute('SELECT COUNT(*) AS total FROM todos WHERE user_id = %s', (user_id,)),
        total = cursor.fetchone()['total']
        return {'data': todos,
        'page': page,
        'limit': limit,
        'total': total,}
    finally:
        conexao.close()

@rota.put('/todos/{todo_id}', response_model=TodoResponse)
def atualizar_todo(
    todo_id: int,
    dados: TodoCreate,
    user_id: int = Depends(get_current_user_id)
):
    conexao = get_connection()
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT user_id FROM todos WHERE id = %s', (todo_id,))
        tarefa = cursor.fetchone()
        if tarefa is None:
            raise HTTPException(status_code=404, detail='Tarefa não encontrada')
        if tarefa['user_id'] != user_id:
            raise HTTPException(status_code=403, detail='Você não pode alterar esta tarefa')
        cursor.execute('UPDATE todos SET title = %s, description = %s WHERE id = %s AND user_id = %s', (dados.title, dados.description, todo_id, user_id))
        conexao.commit()
        return {
            'id': todo_id,
            'title': dados.title,
            'description': dados.description
        }
    finally:
        conexao.close()


from sqlalchemy import select

import models
from database import Base, SessionLocal, engine

# Cria as tabelas no arquivo todo.db (se ainda não existirem)
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    # INSERT de um usuário
    user = models.User(name="José", email="jose@email.com", hashed_password="provisorio")
    db.add(user)
    db.commit()
    db.refresh(user)

    # INSERT de uma tarefa ligada a esse usuário
    todo = models.Todo(title="Comprar pão", description="Pão e leite", owner_id=user.id)
    db.add(todo)
    db.commit()

    # SELECT das tarefas desse usuário
    tarefas = db.scalars(
        select(models.Todo).where(models.Todo.owner_id == user.id)
    ).all()

    for t in tarefas:
        print("TAREFA:", t.id, t.title, "| dono:", t.owner.name)

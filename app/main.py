from fastapi import FastAPI
from app.routers import users, todos

app = FastAPI(title='Todo List API', description='RESTful API to manage to-do lists, with JWT authentication', version='1.0.0')
app.include_router(users.rota)
app.include_router(todos.rota)

@app.get('/', include_in_schema=False)
async def read_root():
    return {"status": "ok"}




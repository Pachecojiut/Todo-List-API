from fastapi import FastAPI
from app.routers import users, todos

app = FastAPI()
app.include_router(users.rota)
app.include_router(todos.rota)

@app.get('/')
async def read_root():
    return {"status": "ok"}



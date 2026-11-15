from fastapi import FastAPI
from app.routers import users

app = FastAPI()
app.include_router(users.rota)

@app.get('/')
async def read_root():
    return {"status": "ok"}


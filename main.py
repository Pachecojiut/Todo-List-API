from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def raiz():
    return {"mensagem": "olá"}


@app.get("/ola/{nome}")
def ola_nome(nome: str):
    return {"mensagem": f"olá, {nome}!"}

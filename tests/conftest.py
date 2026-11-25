import os 

os.environ['DB_NAME'] = 'todo_test'
os.environ['SECRET_KEY'] = 'chave_de_acesso_para_os_testes_com_mais_de_32_caracteres'

import pytest
from app.database import get_connection

@pytest.fixture(autouse=True)
def limpar_banco():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT DATABASE() AS banco')
        banco = cursor.fetchone()['banco']
        if banco != 'todo_test':
            raise RuntimeError(f'Banco incorreto: {banco!r}.' " A fixture só pode limpar o banco 'todo_test'.")

        cursor.execute('DELETE FROM todos')
        cursor.execute('DELETE FROM  users')
        connection.commit()
        cursor.close()
    finally:
        connection.close()


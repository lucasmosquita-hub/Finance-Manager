import sqlite3


def conectar():
    conexao = sqlite3.connect("financeiro.db")
    conexao.row_factory = sqlite3.Row

    return conexao


def criar_tabela():

    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()
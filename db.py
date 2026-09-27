"""
Camada de acesso ao banco de dados do Sistema de Controle de Patrimônio.

Antes de usar, edite os dados de conexão em DB_CONFIG abaixo com o usuário
e senha do seu MySQL local.
"""

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA_AQUI",
    "database": "patrimonio_igreja",
}


def get_connection():
    """Abre e retorna uma conexão com o banco de dados MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


# ---------------------- Departamentos ----------------------

def listar_departamentos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM departamentos ORDER BY nome")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


def adicionar_departamento(nome):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departamentos (nome) VALUES (%s)", (nome,))
    conn.commit()
    cursor.close()
    conn.close()


# ---------------------- Itens ----------------------

def adicionar_item(nome, categoria, valor, data_aquisicao, departamento_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO itens (nome, categoria, valor, data_aquisicao, departamento_id)
           VALUES (%s, %s, %s, %s, %s)""",
        (nome, categoria, valor or None, data_aquisicao or None, departamento_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def listar_itens():
    """Retorna todos os itens com o nome do departamento e status atual."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT i.id, i.nome, i.categoria, i.valor, d.nome, i.status
           FROM itens i
           LEFT JOIN departamentos d ON i.departamento_id = d.id
           ORDER BY i.nome"""
    )
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


def listar_itens_disponiveis():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome FROM itens WHERE status = 'disponivel' ORDER BY nome"
    )
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


def listar_itens_em_uso():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT m.id, i.nome, m.responsavel, m.data_retirada
           FROM movimentacoes m
           JOIN itens i ON m.item_id = i.id
           WHERE m.data_devolucao IS NULL
           ORDER BY m.data_retirada"""
    )
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


# ---------------------- Movimentações ----------------------

def registrar_retirada(item_id, responsavel, observacao=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO movimentacoes (item_id, responsavel, observacao) VALUES (%s, %s, %s)",
        (item_id, responsavel, observacao),
    )
    cursor.execute(
        "UPDATE itens SET status = 'em_uso' WHERE id = %s", (item_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def registrar_devolucao(movimentacao_id, item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE movimentacoes SET data_devolucao = NOW() WHERE id = %s",
        (movimentacao_id,),
    )
    cursor.execute(
        "UPDATE itens SET status = 'disponivel' WHERE id = %s", (item_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def historico_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT responsavel, data_retirada, data_devolucao, observacao
           FROM movimentacoes WHERE item_id = %s ORDER BY data_retirada DESC""",
        (item_id,),
    )
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


# ---------------------- Relatórios ----------------------

def relatorio_por_departamento():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT d.nome, COUNT(i.id) AS total,
                  SUM(CASE WHEN i.status = 'em_uso' THEN 1 ELSE 0 END) AS em_uso
           FROM departamentos d
           LEFT JOIN itens i ON i.departamento_id = d.id
           GROUP BY d.nome
           ORDER BY d.nome"""
    )
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

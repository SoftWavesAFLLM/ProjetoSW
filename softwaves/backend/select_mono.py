from conectar import get_connection
from mysql.connector import Error

def generic_select(table, columns='*', where=None, order_by=None, limit=None, database='softwavesafllm'):
    """
    Executa um SELECT genérico em qualquer tabela.
    
    Parâmetros:
      table (str): Nome da tabela (deve ser validado para evitar injeção).
      columns (str): Colunas a serem retornadas, ex: "id, nome". Padrão '*'.
      where (dict): Dicionário com condições, ex: {"id": 1, "status": "ativo"}.
      order_by (str): Coluna(s) para ordenação.
      limit (int): Limite de registros a retornar.
      database (str): Nome do banco de dados.
      
    Retorna:
      List[dict]: Lista de dicionários com os registros encontrados.
    """
    connection = None
    cursor = None
    try:
        print(database)
        connection = get_connection(database)
        cursor = connection.cursor(dictionary=True)
        print('teste2')
        query = f"SELECT {columns} FROM {table}"
        params = []
        if where:
            conditions = []
            for col, val in where.items():
                conditions.append(f"{col} = %s")
                params.append(val)
            query += " WHERE " + " AND ".join(conditions)
        
        if order_by:
            query += " ORDER BY " + order_by
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results

    except Error as e:
        print("Erro na execução da consulta:", e)
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
'''
# Exemplo de uso:
resultados = generic_select(
    table='usuario', 
    columns='id_usuario, nome, email, telefone, cargo', 
    where={'id_usuario': 1},
    database='base'
)
print(resultados)
'''
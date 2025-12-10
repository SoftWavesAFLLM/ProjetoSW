from conectar import get_connection
from mysql.connector import Error

def generic_join_select(main_table, joins, columns='*', where=None, order_by=None, limit=None, database='softwavesafllm'):
    """
    Executa uma consulta que une várias tabelas.
    
    Parâmetros:
      main_table (str): Nome da tabela principal.
      joins (list): Lista de dicionários com dados do join. Cada dicionário deve conter:
                      - 'type': tipo do join ("INNER", "LEFT", "RIGHT", etc.). Padrão: "INNER".
                      - 'table': nome da tabela a unir.
                      - 'condition': condição de junção (ex: "main_table.id = outra_tabela.id_ref").
      columns (str): Colunas a serem retornadas. Padrão: '*'.
      where (dict): Dicionário com condições para o WHERE, ex: {"status": "aberta"}.
      order_by (str): Coluna(s) para ordenação.
      limit (int): Número máximo de registros a retornar.
      database (str): Nome do banco de dados.
      
    Retorna:
      List[dict]: Lista de dicionários representando os registros retornados.
    """
    connection = None
    cursor = None
    try:
        connection = get_connection(database)
        cursor = connection.cursor(dictionary=True)
        
        query = f"SELECT {columns} FROM {main_table}"
        
        for join in joins:
            join_type = join.get("type", "INNER").upper()
            join_table = join["table"]
            join_condition = join["condition"]
            query += f" {join_type} JOIN {join_table} ON {join_condition}"
        
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
        print("Erro na execução da consulta com JOIN:", e)
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
'''
# Exemplo de uso: listar as ordens da tabela "ordemmanutencao" e suas peças na tabela "pecanaordem"
joins = [
    {
        "type": "LEFT",
        "table": "pecanaordem",
        "condition": "ordemmanutencao.id_ordem = pecanaordem.id_ordem"
    }
]

resultados_join = generic_join_select(
    main_table="ordemmanutencao",
    joins=joins,
    columns="ordemmanutencao.id_ordem, ordemmanutencao.descricao, pecanaordem.id_peca, pecanaordem.quantidade",
    where={"ordemmanutencao.status": "aberta"},
    order_by="ordemmanutencao.data_criacao DESC",
    limit=10,
    database='base'
)

for registro in resultados_join:
    print(registro)
'''
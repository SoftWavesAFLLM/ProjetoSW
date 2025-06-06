import mysql.connector
from mysql.connector import Error

def get_connection(database='softwavesafllm'):
    """
    Retorna uma conexão com o banco de dados informado.
    Parâmetros:
      database (str): Nome do banco de dados a ser utilizado.   
    Retorna:
      connection: Objeto de conexão do mysql.connector.
    """
    #print('base_conn ',database)
    try:
        connection = mysql.connector.connect(
            host='localhost',  # substitua pelo seu host
            user='root',       # substitua pelo seu usuário
            password='',   # substitua pela sua senha
            database='softwavesafllm',   # substitua pelo seu banco de dados
            use_pure=True      # usar a comandos em modo de texto
        )
        if connection.is_connected():
            print("Conexão com o MySQL estabelecida com sucesso!")
        return connection
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None
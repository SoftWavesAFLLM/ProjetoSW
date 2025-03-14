import mysql.connector #Ferramenta(componente) conexão

def connect_banco(): #Função Base
    try: #Tente realizar
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="softwavesafllm"
        )
        return connection #Retorna a conexão dentro da variavel
    except mysql.connector.Error as err: #Em caso de erro gravo o erro da variavel[err]
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None
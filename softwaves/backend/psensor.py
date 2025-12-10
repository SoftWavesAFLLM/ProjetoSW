from conectar import get_connection
import json

def listar_sensores():
    """
    Retorna todos os sensores mais recentes primeiro
    """
    try:
        print("Conectando ao banco...")  # checkpoint 1: tentando conectar
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dados_sensor ORDER BY data_hora DESC")
        resultados = cursor.fetchall()
        print(f"{len(resultados)} registros encontrados")  # checkpoint 2: quantidade de registros
        return resultados
    except Exception as e:
        print("Erro ao listar sensores:", e)  # checkpoint 3: erro
        return {'erro': str(e)}
    finally:
        cursor.close()
        conn.close()
        print("Conexão com o banco encerrada")  # checkpoint 4


def inserir_sensor(topico, valor):
    print('insert', topico, valor)
    """
    valor: dict, ex: {"temperatura": 28, "umidade": 33}
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        valor_str = json.dumps(valor)  # transforma em string JSON
        sql = "INSERT INTO dados_sensor (topico, valor) VALUES (%s, %s)"
        cursor.execute(sql, (topico, valor_str))
        conn.commit()
        return {'status': 'dado inserido'}
    except Exception as e:
        return {'erro': str(e)}
    finally:
        cursor.close()
        conn.close()



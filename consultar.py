from conectar import connect_banco
import mysql.connector

def read_clientes():
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cliente")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar clientes: {err}"}
        finally:
            cursor.close()
            conn.close()
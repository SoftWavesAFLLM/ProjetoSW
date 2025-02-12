from conectar import connect_banco
import mysql.connector

def delete_cliente(idCliente):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM Cliente WHERE idCliente = %s"
            cursor.execute(sql, (idCliente,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Cliente {idCliente} excluido com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir cliente: {err}"}
        finally:
            cursor.close()
            conn.close()
from conectar import connect_banco
import mysql.connector

def update_cliente(dados):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE cliente SET cep = %s, telefone = %s, email = %s WHERE idCliente = %s" #UPDATE sem WHERE não existe
            values = (dados['cep'], dados['telefone'], dados['email'], dados['idCliente'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Cliente {dados['idCliente']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar cliente: {err}"}
        finally:
            cursor.close()
            conn.close()
from conectar import connect_banco
import mysql.connector


#----------------INICIO - Delete Maquina----------------

def delete_maquina(idmaquinas):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM maquinas WHERE idmaquinas = %s"
            cursor.execute(sql, (idmaquinas,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Maquina {idmaquinas} excluida com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir maquina: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Maquina----------------



#----------------INICIO - Delete Usuario----------------

def delete_usuario(idusuario):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM usuarios WHERE idusuario = %s"
            cursor.execute(sql, (idusuario,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Usuario {idusuario} excluido com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir usuario: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Usuario----------------



#----------------INICIO - Delete Sensor----------------

def delete_sensor(idsensores):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM sensores WHERE idsensores = %s"
            cursor.execute(sql, (idsensores,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Sensor {idsensores} excluido com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir sensor: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Sensor----------------



#----------------INICIO - Delete Manutenção----------------

def delete_manutencao(idordens_manutencao):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM ordens_manutencao WHERE idordens_manutencao = %s"
            cursor.execute(sql, (idordens_manutencao,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Ordem de manutencao {idordens_manutencao} excluida com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir ordem de manutencao: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Manutenção----------------



#----------------INICIO - Delete Trabalho em Ordens----------------

def delete_trabalho_ordens(idordens):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM trabalho_ordens WHERE idordens = %s"
            cursor.execute(sql, (idordens,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Trabalho em ordem {idordens} excluido com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir trabalho em ordem: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Trabalho em Ordens----------------



#----------------INICIO - Delete Peças----------------

def delete_peca(idpecas):
    conn = connect_banco()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "DELETE FROM pecas WHERE idpecas = %s"
            cursor.execute(sql, (idpecas,))
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Peça {idpecas} excluida com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao excluir Peça: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Delete Peças----------------
from conectar import get_connection
import mysql.connector


#----------------INICIO - Read Maquinas----------------

def read_maquinas():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM maquinas")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar maquinas: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Maquinas----------------



#----------------INICIO - Read Usuarios----------------

def read_usuarios():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar usuarios: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Usuarios----------------



#----------------INICIO - Read Sensor----------------

def read_sensor():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensores")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar sensor: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Sensor----------------



#----------------INICIO - Read Manutenção----------------

def read_manutencao():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ordens_manutencao")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar ordem de manutencao: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Manutenção----------------



#----------------INICIO - Read Trabalho em Ordens----------------

def read_trabalho_ordens():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trabalho_ordens")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar trabalho em ordem: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Trabalho em Ordens----------------



#----------------INICIO - Read Peças----------------

def read_peca():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pecas")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar Peças: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Peças----------------



#----------------INICIO - Read Detalhes da ordem de manutenção----------------

def read_DOMs():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalhes_ordens_manutencao")
            resultados = cursor.fetchall() #cursor.fetchone
            return {'status': 'sucesso', 'dados': resultados}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao consultar Detalhes da ordem de manutenção: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Read Detalhes da ordem de manutenção----------------
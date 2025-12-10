from conectar import get_connection
import mysql.connector
import base64

#----------------INICIO - Read Maquinas----------------

def read_maquinas():

    conn = get_connection()
    if not conn:
        return {'status': 'erro', 'mensagem': 'Erro ao conectar ao banco'}

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT idmaquinas, nome_maquina, localizacao, status_maquina,
                   DATE_FORMAT(data_instalacao_maquina, '%Y-%m-%d'), fabricante, imagem
            FROM maquinas
        """)
        resultados = cursor.fetchall()

        maquinas = []
        for row in resultados:
            imagem_bytes = row[6]
            imagem_base64 = None
            if imagem_bytes:
                imagem_base64 = f"data:image/jpeg;base64,{base64.b64encode(imagem_bytes).decode('utf-8')}"

            maquinas.append({
                'idmaquinas': row[0],
                'nome_maquina': row[1],
                'localizacao': row[2],
                'status_maquina': row[3],
                'data_instalacao_maquina': row[4],
                'fabricante': row[5],
                'imagem': imagem_base64
            })

        return {'status': 'sucesso', 'maquinas': maquinas}

    except mysql.connector.Error as err:
        return {'status': 'erro', 'mensagem': f'Erro ao consultar máquinas: {err}'}

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
            cursor.execute("SELECT idusuario, nome_usuario, email, cpf_cnpj, telefone, cargo, senha FROM usuarios")
            resultados = cursor.fetchall() #cursor.fetchone

            usuarios = []
            for row in resultados:
                usuario = {
                    'idusuario': row[0],
                    'nome_usuario': row[1],
                    'email': row[2],
                    'cpf_cnpj': row[3],
                    'telefone': row[4],
                    'cargo': row[5],
                    'senha': row[6]
                }
                usuarios.append(usuario)
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
    if not conn:
        return {'status': 'erro', 'mensagem': 'Erro ao conectar ao banco'}
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT idsensores, tipo_sensor, descricao_sensor, 
                   DATE_FORMAT(data_instalacao_sensor, '%Y-%m-%d'),
                   maquinas_idmaquinas, imagem 
            FROM sensores
        """)
            
        resultados = cursor.fetchall()
            
        sensores = []
        for row in resultados:

            imagem_bytes = row[5]

            # ❗ CORREÇÃO 1: NÃO colocar "data:image/jpeg;base64" aqui
            imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8') if imagem_bytes else None

            sensores.append({
                'idsensores': row[0],
                'tipo_sensor': row[1],
                'descricao_sensor': row[2],
                'data_instalacao_sensor': row[3],
                'maquinas_idmaquinas': row[4],
                'imagem': imagem_base64
            })

        # ❗ CORREÇÃO 2: return FORA do loop
        return {'status': 'sucesso', 'dados': sensores}
        
    except mysql.connector.Error as err:
        return {'status': 'erro', 'mensagem': f"Erro ao consultar sensores: {err}"}
        
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
    if not conn:
        return {'status': 'erro', 'mensagem': 'Erro ao conectar ao banco'}
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT idpecas, nome_pecas, codigo_pecas, quantidade, imagem
            FROM pecas
        """)
        resultados = cursor.fetchall() #cursor.fetchone

        pecas = []
        for row in resultados:
            imagem_bytes = row[4]
            imagem_base64 = None
            if imagem_bytes:
                imagem_base64 = f"data:image/jpeg;base64,{base64.b64encode(imagem_bytes).decode('utf-8')}"

            pecas.append({
                'idpecas': row[0],
                'nome_pecas': row[1],
                'codigo_pecas': row[2],
                'quantidade': row[3],
                'imagem': imagem_base64
            })

        return {'status': 'sucesso', 'pecas': pecas}

    except mysql.connector.Error as err:
        return {'status': 'erro', 'mensagem': f'Erro ao consultar peças: {err}'}

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
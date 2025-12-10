from conectar import get_connection
import mysql.connector

def update_maquina(dados):
    conn = get_connection()
    if not conn:
        return {'status': 'erro', 'mensagem': 'Erro ao conectar ao banco'}

    try:
        cursor = conn.cursor()

        imagem_bytes = dados.get("imagem")

        sql = """
            UPDATE maquinas
            SET nome_maquina = %s,
                localizacao = %s,
                status_maquina = %s,
                data_instalacao_maquina = %s,
                fabricante = %s
            WHERE idmaquinas = %s
        """

        values = (
            dados['nome_maquina'],
            dados['localizacao'],
            dados['status_maquina'],
            dados['data_instalacao_maquina'],
            dados['fabricante'],
            dados['idmaquinas']
        )

        cursor.execute(sql, values)
        conn.commit()

        return {'status': 'sucesso', 'mensagem': f"Máquina {dados['idmaquinas']} atualizada com sucesso."}

    except mysql.connector.Error as err:
        return {'status': 'erro', 'mensagem': f"Erro ao atualizar máquina: {err}"}

    finally:
        cursor.close()
        conn.close()


#----------------INICIO - Update Usuario----------------

def update_usuario(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE usuarios SET nome_usuario = %s, email = %s, cpf_cnpj = %s, telefone = %s, cargo = %s, senha = %s WHERE idusuario = %s" #UPDATE sem WHERE não existe
            values = (dados['nome_usuario'], dados['email'], dados['cpf_cnpj'], dados['telefone'], dados['cargo'], dados['senha'], dados['idusuario'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Usuario {dados['idusuario']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar usuario: {err}"}
        finally:
            cursor.close()
            conn.close()
            
#----------------FIM - Update Usuario----------------



#----------------INICIO - Update Sensores------------------

def update_sensor(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE sensores SET tipo_sensor = %s, descricao_sensor = %s, data_instalacao_sensor = %s, maquinas_idmaquinas = %s WHERE idsensores = %s" #UPDATE sem WHERE não existe
            values = (dados['tipo_sensor'], dados['descricao_sensor'], dados['data_instalacao_sensor'], dados['maquinas_idmaquinas'], dados['idsensores'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Sensor {dados['idsensores']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar sensor: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Update  Sensores----------------



#----------------INICIO - Update Manutenção----------------

def update_manutencao(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE ordens_manutencao SET descricao_problema = %s, tipo_manutencao = %s, status_manutencao = %s, maquinas_idmaquinas = %s, usuarios_idusuario = %s WHERE idordens_manutencao = %s" #UPDATE sem WHERE não existe
            values = (dados['descricao_problema'],  dados['tipo_manutencao'], dados['status_manutencao'], dados['maquinas_idmaquinas'], dados['usuarios_idusuario'], dados['idordens_manutencao'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Ordem de manutencao {dados['idordens_manutencao']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar ordem de manutencao: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Update Manutenção----------------



#----------------INICIO - Update Trabalho em Ordens----------------

def update_trabalho_ordens(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE trabalho_ordens SET descricao_manutencao = %s, status_ordem = %s, tipo_manutencao = %s, data_criacao = %s, data_conclusao = %s, ordens_manutencao_idordens_manutencao = %s, usuarios_idusuario = %s WHERE idordens = %s" #UPDATE sem WHERE não existe
            values = (dados['descricao_manutencao'], dados['status_ordem'], dados['tipo_manutencao'], dados['data_criacao'], dados['data_conclusao'], dados['ordens_manutencao_idordens_manutencao'], dados['usuarios_idusuario'], dados['idordens'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Trabalho na ordem {dados['idordens']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar trabalho na ordem: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Update Trabalho em Ordens----------------



#----------------INICIO - Update Peça----------------

def update_peca(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE pecas SET nome_pecas = %s, codigo_pecas = %s, quantidade = %s WHERE idpecas = %s" #UPDATE sem WHERE não existe
            values = (dados['nome_pecas'], dados['codigo_pecas'], dados['quantidade'], dados['idpecas'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Peça {dados['idpecas']} atualizada com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar Peça: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Update Peça----------------



#----------------INICIO - Update Detalhes da ordem de manutenção----------------

def update_DOM(dados):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "UPDATE detalhes_ordens_manutencao SET quantidade = %s, ordens_manutencao_idordens_manutencao = %s, pecas_idpecas WHERE iddetalhes_ordens_manutencao = %s" #UPDATE sem WHERE não existe
            values = (dados['quantidade'], dados['ordens_manutencao_idordens_manutencao'], dados['pecas_idpecas'], dados['iddetalhes_ordens_manutencao'])
            print('Antes update:', values)
            cursor.execute(sql, values)
            conn.commit()
            return {'status': 'sucesso', 'mensagem': f"Detalhes da ordem de manutenção {dados['iddetalhes_ordens_manutencao']} atualizado com sucesso."}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao atualizar detalhes da ordem de manutenção: {err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Update Detalhes da ordem de manutenção----------------

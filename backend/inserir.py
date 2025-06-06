from conectar import get_connection #Importação componente de conexão
import mysql.connector


#--------------INICIO - Insert Maquina--------------

def insert_maquina(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO maquinas (nome_maquina, localizacao, status_maquina, data_instalacao_maquina, fabricante) VALUES (%s, %s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['nome_maquina'], dados['localizacao'], dados['status_maquina'], dados['data_instalacao_maquina'], dados['fabricante']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Maquina cadastrada com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar maquina:{err}"}
        finally:
            cursor.close()
            conn.close()

#--------------FIM - Insert Maquina--------------



#--------------INICIO - Insert Usuario----------------

def insert_usuario(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO usuarios (nome_usuario, email, cpf_cnpj, telefone, cargo, senha) VALUES (%s, %s, %s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['nome_usuario'], dados['email'], dados['cpf_cnpj'], dados['telefone'], dados['cargo'], dados['senha']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Usuario cadastrado com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar usuario:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Usuario----------------



#----------------INICIO - Insert Sensor----------------

def insert_sensor(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO sensores (tipo_sensor, descricao_sensor, data_instalacao_sensor, maquinas_idmaquinas) VALUES (%s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['tipo_sensor'], dados['descricao_sensor'], dados['data_instalacao_sensor'], dados['maquinas_idmaquinas']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Sensor cadastrado com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar sensor:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Sensor----------------



#----------------INICIO - Insert Manutenção----------------

def insert_manutencao(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO ordens_manutencao (descricao_problema, tipo_manutencao, status_manutencao, maquinas_idmaquinas, usuarios_idusuario) VALUES (%s, %s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['descricao_problema'], dados['tipo_manutencao'], dados['status_manutencao'], dados['maquinas_idmaquinas'], dados['usuarios_idusuario']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Manutenção registrada com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao registrar manutenção:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Manutenção-----------------



#----------------INICIO - Insert Trabalho em Ordens----------------

def insert_trabalho_ordens(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão    
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO trabalho_ordens (descricao_manutencao, status_ordem, tipo_manutencao, data_criacao, data_conclusao, ordens_manutencao_idordens_manutencao, usuarios_idusuario) VALUES (%s, %s, %s, %s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['descricao_manutencao'], dados['status_ordem'], dados['tipo_manutencao'], dados['data_criacao'], dados['data_conclusao'], dados['ordens_manutencao_idordens_manutencao'], dados['usuarios_idusuario']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Trabalho em ordem cadastrado com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar trabalho em ordens:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Trabalho em Ordens----------------



#----------------INICIO - Insert Peça----------------

def insert_peca(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO pecas (nome_pecas, codigo_pecas, quantidade) VALUES (%s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['nome_pecas'], dados['codigo_pecas'], dados['quantidade']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Peça cadastrada com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar peça:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Peça----------------



#----------------INICIO - Insert Detalhes da ordem de manutenção----------------

def insert_DOM(dados): #Criação da função + parametros
    conn = get_connection() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO detalhes_ordens_manutencao (quantidade, ordens_manutencao_idordens_manutencao, pecas_idpecas) VALUES (%s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['quantidade'], dados['ordens_manutencao_idordens_manutencao'], dados['pecas_idpecas']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Detalhes da ordem de manutenção cadastrado com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar detalhes da ordem de manutenção:{err}"}
        finally:
            cursor.close()
            conn.close()

#----------------FIM - Insert Detalhes da ordem de manutenção----------------
from conectar import connect_banco #Importação componente de conexão
import mysql.connector

def insert_cliente(dados): #Criação da função + parametros
    conn = connect_banco() #Variavel recebe obj da conexão
    if conn: #Verifico a variavel
        try:
            cursor = conn.cursor() #Atribuir o cursor(apontamento) a uma variavel
            sql = "INSERT INTO cliente (nome, cep, telefone, email, cpf) VALUES (%s, %s, %s, %s, %s)" #Criação do sql com parametros por posição
            values = (dados['nome'], dados['cep'], dados['telefone'], dados['email'], dados['cpf']) #Valores a serem gravados
            print('Antes insert:', values)
            cursor.execute(sql, values) #Executar o comando
            conn.commit() #Confirmo o executar
            return {'status': 'sucesso', 'mensagem': 'Cliente cadastrado com sucesso.'}
        except mysql.connector.Error as err:
            return {'status': 'erro', 'mensagem': f"Erro ao cadastrar cliente:{err}"}
        finally:
            cursor.close()
            conn.close()
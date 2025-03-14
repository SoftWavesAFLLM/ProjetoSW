from validacao import validacao
from preparacao_gravacao import preparar_usuario_para_gravacao, preparar_maquina_para_gravacao, preparar_sensor_para_gravacao, preparar_odmanutencao_para_gravacao, preparar_trabalho_ordens_para_gravacao, preparar_peca_para_gravacao
from inserir import insert_usuario, insert_maquina, insert_sensor, insert_manutencao, insert_trabalho_ordens, insert_peca
from atualizar import update_usuario, update_maquina, update_sensor, update_manutencao, update_trabalho_ordens, update_peca
from consultar import read_usuarios, read_maquinas, read_sensor, read_manutencao, read_trabalho_ordens, read_peca
from deletar import delete_usuario, delete_maquina, delete_sensor, delete_manutencao, delete_trabalho_ordens, delete_peca


#----------INICIO - Processamento Maquina----------
def processar_maquina(acao, dados=None):
    resposta = {}
    print("Processar maquina:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_maquina', 'atualizar_maquina']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_maquina_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_maquina':
            resposta = insert_maquina(dados_preparados)
        elif acao == 'atualizar_maquina':
            resposta = update_maquina(dados_preparados)
        #Ação de listar maquinas
    
    elif acao == 'listar_maquinas':
        resposta = read_maquinas()

    #Ação de deletar maquina
    elif acao == 'excluir_maquina':
        resposta = delete_maquina(dados['idmaquinas'])

    return resposta

#----------FIM - Processamento Maquina---------- 



#----------INICIO - Processamento Usuario----------

def processar_usuario(acao, dados=None):
    resposta = {}
    print("Processar usuario:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_usuario', 'atualizar_usuario']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_usuario_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_usuario':
            resposta = insert_usuario(dados_preparados)
        elif acao == 'atualizar_usuario':
            resposta = update_usuario(dados_preparados)
        
    #Ação de listar usuarios
    elif acao == 'listar_usuarios':
        resposta = read_usuarios()

    #Ação de deletar usuario
    elif acao == 'excluir_usuario':
        resposta = delete_usuario(dados['idusuario'])

    return resposta    

#----------FIM - Processamento Usuario----------
        


#----------INICIO - Processamento Sensores----------

def processar_sensor(acao, dados=None):
    resposta = {}
    print("Processar sensor:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['insert_sensor', 'update_sensor']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_sensor_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'insert_sensor':
            resposta = insert_sensor(dados_preparados)
        elif acao == 'update_sensor':
            resposta = update_sensor(dados_preparados)
        #Ação de listar clientes
    
    elif acao == 'read_sensor':
        resposta = read_sensor()

    #Ação de deletar clientes
    elif acao == 'delete_sensor':
        resposta = delete_sensor(dados['idsensores'])

    return resposta

#----------FIM - Processamento Sensores----------



#----------INICIO - Processamento Manutenção----------

def processar_odmanutencao(acao, dados=None):
    resposta = {}
    print("Processar manutencao:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_odmanutencao', 'atualizar_odmanutencao']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_odmanutencao_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_odmanutencao':
            resposta = insert_manutencao(dados_preparados)
        elif acao == 'atualizar_odmanutencao':
            resposta = update_manutencao(dados_preparados)
        #Ação de listar ordens de manutenção
    
    elif acao == 'listar_odmanutencao':
        resposta = read_manutencao()

    #Ação de deletar ordem de manutenção
    elif acao == 'excluir_odmanutencao':
        resposta = delete_manutencao(dados['idordens_manutencao'])
        
    return resposta

#----------FIM - Processamento Manutenção----------



#----------INICIO - Processamento Trabalho em Ordens----------

def processar_trabalho_ordens(acao, dados=None):
    resposta = {}
    print("Processar trabalho em ordens:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_trabalho_ordens', 'atualizar_trabalho_ordens']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_trabalho_ordens_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_trabalho_ordens':
            resposta = insert_trabalho_ordens(dados_preparados)
        elif acao == 'atualizar_trabalho_ordens':
            resposta = update_trabalho_ordens(dados_preparados)
        #Ação de listar trabalho em ordens
    
    elif acao == 'listar_trabalho_ordens':
        resposta = read_trabalho_ordens()

    #Ação de deletar trabalho em ordens
    elif acao == 'excluir_trabalho_ordens':
        resposta = delete_trabalho_ordens(dados['idordens'])

    return resposta

#----------FIM - Processamento Trabalho em Ordens----------



#----------INICIO - Processamento Peças----------

def processar_peca(acao, dados=None):
    resposta = {}
    print("Processar peças:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_peca', 'atualizar_peca']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_peca_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_peca':
            resposta = insert_peca(dados_preparados)
        elif acao == 'atualizar_peca':
            resposta = update_peca(dados_preparados)
        #Ação de listar trabalho em ordens
    
    elif acao == 'listar_pecas':
        resposta = read_peca()

    #Ação de deletar trabalho em ordens
    elif acao == 'excluir_peca':
        resposta = delete_peca(dados['idpecas'])

    return resposta

#----------FIM - Processamento Peças----------
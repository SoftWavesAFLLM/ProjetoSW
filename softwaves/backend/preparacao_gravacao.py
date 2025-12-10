import base64

def preparar_maquina_para_gravacao(acao, dados):
    imagem_bytes = dados.get('imagem')  # já é bytes do endpoint

    if acao == 'criar_maquina':
        return {
            'nome_maquina': dados['nome_maquina'],
            'localizacao': dados['localizacao'],
            'status_maquina': dados['status_maquina'],
            'data_instalacao_maquina': dados['data_instalacao_maquina'],
            'fabricante': dados['fabricante'],
            'imagem': imagem_bytes  # bytes já prontos
        }

    elif acao == 'atualizar_maquina':
        return {
            'idmaquinas': dados['idmaquinas'],
            'nome_maquina': dados['nome_maquina'],
            'localizacao': dados['localizacao'],
            'status_maquina': dados['status_maquina'],
            'data_instalacao_maquina': dados['data_instalacao_maquina'],
            'fabricante': dados['fabricante'],
            'imagem': imagem_bytes  # bytes já prontos
        }

    


#------INICIO - Preparação para gravação Usuario------

def preparar_usuario_para_gravacao(acao, dados):
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_usuario':
        return {
            'nome_usuario': dados['nome_usuario'],
            'email': dados['email'],
            'cpf_cnpj': dados['cpf_cnpj'],
            'telefone': dados['telefone'],
            'cargo': dados['cargo'],
            'senha': dados['senha']
        }
    
    elif acao == 'atualizar_usuario':
        return {
            'idusuario': dados['idusuario'],
            'nome_usuario': dados['nome_usuario'],
            'email': dados['email'],
            'cpf_cnpj': dados['cpf_cnpj'],
            'telefone': dados['telefone'],
            'cargo': dados['cargo'],
            'senha': dados['senha']
        }

#------FIM - Preparação para gravação Usuario------



#------INICIO - Preparação para gravação Sensores------

def preparar_sensor_para_gravacao(acao, dados):
    imagem_bytes = dados.get('imagem')  # já é bytes do endpoint
    
    if acao == 'insert_sensor':
        return {
            'tipo_sensor': dados['tipo_sensor'],
            'descricao_sensor': dados['descricao_sensor'],
            'data_instalacao_sensor': dados['data_instalacao_sensor'],
            'maquinas_idmaquinas': dados['maquinas_idmaquinas'],
            'imagem': imagem_bytes  # bytes já prontos
        }
    
    elif acao == 'update_sensor':
        return {
            'idsensores': dados['idsensores'],
            'tipo_sensor': dados['tipo_sensor'],
            'descricao_sensor': dados['descricao_sensor'],
            'data_instalacao_sensor': dados['data_instalacao_sensor'],
            'maquinas_idmaquinas': dados['maquinas_idmaquinas'],
            'imagem': imagem_bytes  # bytes já prontos
        }

#------FIM - Preparação para gravação Sensores------



#------INICIO - Preparação para gravação Manutenção------

def preparar_odmanutencao_para_gravacao(acao, dados):
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_odmanutencao':
        return {
            'descricao_problema': dados['descricao_problema'],
            'tipo_manutencao': dados['tipo_manutencao'],
            'status_manutencao': dados['status_manutencao'],
            'maquinas_idmaquinas': dados['maquinas_idmaquinas'],
            'usuarios_idusuario': dados['usuarios_idusuario']
        }
    
    elif acao == 'atualizar_odmanutencao':
        return {
            'idordens_manutencao': dados['idordens_manutencao'],
            'descricao_problema': dados['descricao_problema'],
            'tipo_manutencao': dados['tipo_manutencao'],
            'status_manutencao': dados['status_manutencao'],
            'maquinas_idmaquinas': dados['maquinas_idmaquinas'],
            'usuarios_idusuario': dados['usuarios_idusuario']
        }

#------FIM - Preparação para gravação Manutenção------



#------INICIO - Preparação para gravação Trabalho em Ordens------

def preparar_trabalho_ordens_para_gravacao(acao, dados):
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_trabalho_ordens':
        return {
            'descricao_manutencao': dados['descricao_manutencao'],
            'status_ordem': dados['status_ordem'],
            'tipo_manutencao': dados['tipo_manutencao'],
            'data_criacao': dados['data_criacao'],
            'data_conclusao': dados['data_conclusao'],
            'ordens_manutencao_idordens_manutencao': dados['ordens_manutencao_idordens_manutencao'],
            'usuarios_idusuario': dados['usuarios_idusuario']
        }
    
    elif acao == 'atualizar_trabalho_ordens':
        return {
            'idordens': dados['idordens'],
            'descricao_manutencao': dados['descricao_manutencao'],
            'status_ordem': dados['status_ordem'],
            'tipo_manutencao': dados['tipo_manutencao'],
            'data_criacao': dados['data_criacao'],
            'data_conclusao': dados['data_conclusao'],
            'ordens_manutencao_idordens_manutencao': dados['ordens_manutencao_idordens_manutencao'],
            'usuarios_idusuario': dados['usuarios_idusuario']
        }

#------FIM - Preparação para gravação Trabalho em Ordens------



#------INICIO - Preparação para gravação Peças------

def preparar_peca_para_gravacao(acao, dados):
    imagem_bytes = dados.get('imagem')  # já é bytes do endpoint
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_peca':
        return {
            'nome_pecas': dados['nome_pecas'],
            'codigo_pecas': dados['codigo_pecas'],
            'quantidade': dados['quantidade'],
            'imagem': imagem_bytes  # bytes já prontos
        }
    
    elif acao == 'atualizar_peca':
        return {
            'idpecas': dados['idpecas'],
            'nome_pecas': dados['nome_pecas'],
            'codigo_pecas': dados['codigo_pecas'],
            'quantidade': dados['quantidade'],
            'imagem': imagem_bytes  # bytes já prontos
        }

#------FIM - Preparação para gravação Peças------



#------INICIO - Preparação para gravação Detalhes da ordem de manutenção------

def preparar_DOM_para_gravacao(acao, dados):
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_DOM':
        return {
            'quantidade': dados['quantidade'],
            'ordens_manutencao_idordens_manutencao': dados['ordens_manutencao_idordens_manutencao'],
            'pecas_idpecas': dados['pecas_idpecas']
        }
    
    elif acao == 'atualizar_DOM':
        return {
            'iddetalhes_ordens_manutencao': dados['iddetalhes_ordens_manutencao'],
            'quantidade': dados['quantidade'],
            'ordens_manutencao_idordens_manutencao': dados['ordens_manutencao_idordens_manutencao'],
            'pecas_idpecas': dados['pecas_idpecas']
        }

#------FIM - Preparação para gravação Detalhes da ordem de manutenção------
def validacao(dados):
    erros = []
    print('Validação: ', dados)


#----------------INICIO - Validação Maquina----------------

    if 'nome_maquina' in dados and len(dados['nome_maquina']) == 0: 
        erros.append('Nome da maquina Invalida')

    if 'localizacao' in dados and len(dados['localizacao']) == 0:
        erros.append('Local da maquina Invalido')

    if 'status_maquina' in dados and len(dados['status_maquina']) == 0:
        erros.append('Status da maquina Invalido')

    if 'data_inatalacao_maquina' in dados and len(dados['data_instalacao_maquina']) == 0:
        erros.append('Data de instlação Invalida')
    
    if 'fabricante' in dados and len(dados['fabricante']) == 0:
        erros.append('Fabricante Invalido')

#----------------FIM - Validação Maquina----------------



#----------------INICIO - Validação Usuario----------------

    if 'nome_usuario' in dados and len(dados['nome_usuario']) == 0: 
        erros.append('Nome de usuario Invalido')

    if 'email' in dados and '@' not in dados['email']:
        erros.append('Email Invalido')

    if 'telefone' in dados and len(dados['telefone']) != 11:
        erros.append('Telefone Invalido')
    
    if 'cargo' in dados and len(dados['cargo']) == 0:
        erros.append('Cargo Invalido')

#----------------FIM - Validação Usuario----------------



#----------------INICIO - Validação Sensores----------------

    if 'tipo_sensor' in dados and len(dados['tipo_sensor']) == 0:
        erros.append('Tipo de sensor Invalido')

    if 'descricao_sensor' in dados and len(dados['descricao_sensor']) == 0:
        erros.append('Descrição sensor Invalido')

    if 'data_instalacao_sensor' in dados and len(dados['data_instalacao_sensor']) == 0:
        erros.append('Data de instalação Invalida')

    if 'maquinas_idmaquinas' in dados and dados['maquinas_idmaquinas'] == 0:
        erros.append('Maquina Invalida')

#----------------FIM - Validação Sensores----------------



#----------------INICIO - Validação Manutenção----------------

    #Validar a descrição da manutenção
    if 'descricao_problema' in dados and len(dados['descricao_problema']) == 0: 
        erros.append('Descricao Invalida')

    #Validar status da ordem de manutenção
    if 'status_manutencao' in dados and len(dados['status_manutencao']) == 0: 
        erros.append('Status Invalida')

    #Validar o tipo de manutenção
    if 'tipo_manutencao' in dados and len(dados['tipo_manutencao']) == 0: 
        erros.append('Tipo de Manutenção Invalida')

    if 'maquinas_idmaquinas' in dados and dados['maquinas_idmaquinas'] == 0: 
        erros.append('Maquina Invalida')

    if 'usuario_idusuario' in dados and dados['usuario_idusuario'] == 0: 
        erros.append('Usuario Invalido')

#----------------FIM - Validação Manutenção----------------



#----------------INICIO - Validação Trabalho em Ordens----------------

    if 'descricao_manutencao' in dados and len(dados['descricao_manutencao']) == 0: 
        erros.append('Descrição da manutenção Invalida')

    if 'status_ordem' in dados and len(dados['status_ordem']) == 0:
        erros.append('Status da ordem Invalido')

    if 'tipo_manutencao' in dados and len(dados['tipo_manutencao']) == 0:
        erros.append('Tipo de manutencao Invalido')

    if 'data_criacao' in dados and dados['data_criacao'] == 0:
        erros.append('Data de criação Invalida')
    
    if 'data_conclusao' in dados and dados['data_conclusao'] == 0:
        erros.append('Data de conclusão Invalido')

    if 'ordens_manutencao_idordens_manutencao' in dados and dados['ordens_manutencao_idordens_manutencao'] == 0:
        erros.append('Ordem de manutenção Invalido')

    if 'usuarios_idusuario' in dados and dados['usuarios_idusuario'] == 0:
        erros.append('Usuario Invalido')

#----------------FIM - Validação Trabalho em Ordens----------------



#----------------INICIO - Validação Peça----------------

    #Validar o nome da peça
    if 'nome_pecas' in dados and len(dados['nome_pecas']) == 0: 
        erros.append('Nome da peça Invalido')

    #Validar o codigo da peça
    if 'codigo_pecas' in dados and len(dados['codigo_pecas']) == 0: 
        erros.append('Codigo da peça Invalido')

#----------------FIM - Validação Peça----------------


    return erros if erros else None
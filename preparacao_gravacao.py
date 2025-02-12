def preparar_cliente_para_gravacao(acao, dados):
    print('Preparação: ', dados)#Conferir se o dado chegou
    if acao == 'criar_cliente':
        return {
            'nome': dados['nome'],
            'cep': dados['cep'],
            'telefone': dados['telefone'],
            'email': dados['email'],
            'cpf': dados['cpf']
        }
    
    elif acao == 'atualizar_cliente':
        return {
            'idCliente': dados['idCliente'],
            'cep': dados['cep'],
            'telefone': dados['telefone'],
            'email': dados['email']
        }
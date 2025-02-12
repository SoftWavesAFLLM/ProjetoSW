def validacao(dados):
    erros = []
    print('Validação: ', dados)

    if 'nome' in dados and len(dados['nome']) == 0: 
        erros.append('Nome Invalido')

    if 'cep' in dados and len(dados['cep']) == 0:
        erros.append('CEP Invalido')

    if 'telefone' in dados and len(dados['telefone']) != 11:
        erros.append('Telefone Invalido')

    if 'email' in dados and '@' not in dados['email']:
        erros.append('Email Invalido')
    
    if 'cpf' in dados and len(dados['cpf']) != 11:
        erros.append('CPF ou CNPJ Invalido')

    return erros if erros else None
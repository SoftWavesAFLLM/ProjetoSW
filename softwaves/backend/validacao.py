import urllib.parse
import requests
import re
from datetime import datetime


def validacao(dados):
    
    erros = []



#----------------INICIO - Validação Maquina----------------

    if 'nome_maquina' in dados:
        pattern_nome_maquina = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\-\']{2,100}$"
        nome_maquina = dados['nome_maquina']

        if not re.match(pattern_nome_maquina, nome_maquina):
            erros.append('Nome da máquina inválido. Deve conter 2 a 100 caracteres com letras, números, espaços, hífen ou apóstrofo.')

    if 'localizacao' in dados:
        pattern_localizacao = r'^[A-Za-z0-9À-ÖØ-öø-ÿ\s,.-]{2,100}$'
        localizacao = dados['localizacao']

        if not re.match(pattern_localizacao, localizacao):
            erros.append('Localização da máquina inválida. Use 2 a 100 caracteres, podendo conter letras, números, espaços, vírgulas, pontos e hífens.')


    if 'status_maquina' in dados:
        status = dados['status_maquina']
        pattern_status_maquina = r'^(Em funcionamento|Em manutenção|Inativa)$'

        if not re.match(pattern_status_maquina, status):
            erros.append('Status da máquina inválido')

    if 'data_instalacao_maquina' in dados:
        data = dados['data_instalacao_maquina']

        try:
            # Tenta converter a string para data no formato ISO
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append('Data de instalação Invalida')
    
    if 'fabricante' in dados:
        pattern_fabricante = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]{2,100}$'
        fabricante = dados['fabricante']

        if not re.match(pattern_fabricante, fabricante):
            erros.append('Fabricante inválido. Deve conter 2 a 100 letras e espaços.')


    


#----------------FIM - Validação Maquina----------------



#----------------INICIO - Validação Usuario----------------

    if 'nome_usuario' in dados:
        pattern_nome = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]{2,100}$'
        nome = dados['nome_usuario']

        if not re.match(pattern_nome, nome):
            erros.append('Nome de usuário inválido. Use 2 a 100 letras e espaços.')


    if 'email' in dados:
        email_resultado = validar_email(dados['email'], '18016|OC76VqJYdyDR0GyyZiz7boRw4V04hLDs')
        if email_resultado == False:
            erros.append('Email Invalido')

    if 'cpf_cnpj' in dados:
        cpf_resultado = validar_cpf(cpf=dados['cpf_cnpj'], token='18016|OC76VqJYdyDR0GyyZiz7boRw4V04hLDs')
        if cpf_resultado == False:
            erros.append('CPF Invalido')
    
    if 'telefone' in dados:
        pattern_telefone = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        telefone = dados['telefone']
    
        if not re.match(pattern_telefone, telefone):
            erros.append('Telefone inválido. Use formato com DDD, ex: (11) 99999-9999.')
    
    if 'cargo' in dados:
        pattern_cargo = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]{2,50}$'
        cargo = dados['cargo']

        if not re.match(pattern_cargo, cargo):
            erros.append('Cargo inválido. Use 2 a 50 letras e espaços.')

    if 'senha' in dados:
        pattern_senha = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$'
        senha = dados['senha']

        if not re.match(pattern_senha, senha):
            erros.append('Senha inválida. Deve conter pelo menos 8 caracteres, incluindo letras e números.')


#----------------FIM - Validação Usuario----------------



#----------------INICIO - Validação Sensores----------------

    if 'tipo_sensor' in dados and len(dados['tipo_sensor']) == 0:
        erros.append('Tipo de sensor inválido. Campo não pode estar vazio.')

    if 'descricao_sensor' in dados and len(dados['descricao_sensor']) == 0:
        erros.append('Descrição do sensor inválida. Campo não pode estar vazio.')

    if 'data_instalacao_sensor' in dados:
        data = dados['data_instalacao_sensor']

        try:
            # Tenta converter a string para data no formato ISO
            datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            erros.append('Data de instalação do sensor Invalida')

    if 'maquinas_idmaquinas' in dados and dados['maquinas_idmaquinas'] == 0:
        erros.append('Máquina inválida. Maquina Inexistente.')

#----------------FIM - Validação Sensores----------------



#----------------INICIO - Validação Manutenção----------------

    #Validar a descrição da manutenção
    if 'descricao_problema' in dados and len(dados['descricao_problema']) == 0: 
        erros.append('Descrição inválida. Campo não pode estar vazio.')

    #Validar status da ordem de manutenção
    if 'status_manutencao' in dados:
        status = dados['status_manutencao']
        pattern_status_ordem = r'^(Pendente|Em andamento|Concluída|Cancelada)$'

        if not re.match(pattern_status_ordem, status):
            erros.append('Status da ordem inválido')

    #Validar o tipo de manutenção
    if 'tipo_manutencao' in dados:
        tipo = dados['tipo_manutencao']
        pattern_tipo_manutencao = r'^(Preventiva|Corretiva|Preditiva)$'

        if not re.match(pattern_tipo_manutencao, tipo):
            erros.append('Tipo de manutenção inválido')

    if 'maquinas_idmaquinas' in dados and dados['maquinas_idmaquinas'] == 0: 
        erros.append('Maquina Invalida. Maquina Inexistente')

    if 'usuario_idusuario' in dados and dados['usuario_idusuario'] == 0: 
        erros.append('Usuario Invalido. Usuario Inexistente')

#----------------FIM - Validação Manutenção----------------



#----------------INICIO - Validação Trabalho em Ordens----------------

    if 'descricao_manutencao' in dados and len(dados['descricao_manutencao']) == 0: 
        erros.append('Descrição inválida. Campo não pode estar vazio.')

    if 'status_ordem' in dados:
        status = dados['status_ordem']
        pattern_status_trabalho = r'^(Aberta|Em andamento|Concluída|Cancelada)$'

        if not re.match(pattern_status_trabalho, status):
            erros.append('Status do trabalho na ordem inválido')

    if 'data_criacao' in dados:
        data = dados['data_criacao']

        try:
            datetime.strptime(data, '%Y-%m-%d')
        except (ValueError, TypeError):
            erros.append('Data de criação inválida')
    
    if 'data_conclusao' in dados:
        data = dados['data_conclusao']

        try:
            datetime.strptime(data, '%Y-%m-%d')
        except (ValueError, TypeError):
            erros.append('Data de conclusão inválida')

    if 'ordens_manutencao_idordens_manutencao' in dados and dados['ordens_manutencao_idordens_manutencao'] == 0:
        erros.append('Ordem de manutenção Invalido. Ordem de Manutenção Inexistente')

    if 'usuarios_idusuario' in dados and dados['usuarios_idusuario'] == 0:
        erros.append('Usuario Invalido. Usuario Inexistente')

#----------------FIM - Validação Trabalho em Ordens----------------



#----------------INICIO - Validação Peça----------------

    #Validar o nome da peça
    if 'nome_pecas' in dados:
        pattern_nome_peca = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s\-\']{2,100}$"
        nome_peca = dados['nome_pecas']

        if not re.match(pattern_nome_peca, nome_peca):
            erros.append('Nome da peça inválido. Deve conter 2 a 100 caracteres com letras, números, espaços, hífen ou apóstrofo.')

    #Validar o codigo da peça
    if 'codigo_pecas' in dados:
        pattern_codigo_peca = r'^[A-Za-z0-9-]+$'
        codigo_peca = dados['codigo_pecas']

        if not re.match(pattern_codigo_peca, codigo_peca):
            erros.append('Código da peça inválido. Apenas letras, números e hífen são permitidos.')


#----------------FIM - Validação Peça----------------


    return erros if erros else None

def validar_cpf(cpf, token):
    # URL base da API
    url = "https://api.invertexto.com/v1/validator"

    # Parâmetros que serão enviados via query string
    params = {
        "token": token,
        "value": cpf,  # No exemplo, 'value' representa o CPF
    }

    try:
        # Envia a requisição GET com os parâmetros
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta exceção para status HTTP de erro

        # Converte a resposta para JSON
        data = response.json()
        
        if data['valid'] == False:
            return False

    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro:", err)




def validar_email(email, token):
    # URL base da API de validação de e-mail
    base_url = "https://api.invertexto.com/v1/email-validator"

    # Codifica o e-mail para garantir que a URL fique correta
    email_encoded = urllib.parse.quote(email)

    # Monta a URL com o e-mail na rota
    url = f"{base_url}/{email_encoded}"

    # Parâmetros da query string (neste caso, apenas o token)
    params = {"token": token}

    try:
        # Realiza a requisição GET passando os parâmetros na URL
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta exceção para status HTTP de erro

        # Converte a resposta para JSON
        data = response.json()
        if data['valid_format'] == False or data['valid_mx'] == False or data['disposable'] == True:
            return False

    except requests.exceptions.HTTPError as errh:
        print("Erro HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Erro de conexão:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout:", errt)
    except requests.exceptions.RequestException as err:
        print("Erro:", err)
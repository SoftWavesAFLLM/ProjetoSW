from validacao import validacao
from preparacao_gravacao import preparar_cliente_para_gravacao
from inserir import insert_cliente
from atualizar import update_cliente
from consultar import read_clientes
from deletar import delete_cliente

def processar_cliente(acao, dados=None):
    resposta = {}
    print("Processar cliente:", dados) #Conferir se o dado chegou

    #Verifica se a ação é de criação ou atualização e envia para validações
    if acao in ['criar_cliente', 'atualizar_cliente']:
        erros = validacao(dados)
        if erros:
            return {'status': 'erro', 'mensagem': erros}
        
        #Prepara os dados após a validação
        dados_preparados = preparar_cliente_para_gravacao(acao, dados)

        #Chama o componente de inserção ou atualização
        if acao == 'criar_cliente':
            resposta = insert_cliente(dados_preparados)
        elif acao == 'atualizar_cliente':
            resposta = update_cliente(dados_preparados)
        #Ação de listar clientes
    
    elif acao == 'listar_clientes':
        resposta = read_clientes()

    #Ação de deletar clientes
    elif acao == 'excluir_cliente':
        resposta = delete_cliente(dados['idcliente'])
        
    return resposta
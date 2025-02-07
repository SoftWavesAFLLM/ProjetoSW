from flask import Flask, request, jsonify
from processamento import processar_cliente

app = Flask(__name__)


#Rota para criação de novos clientes
@app.route('/cliente', methods=['POST'])
def criar_cliente():
    dados = request.json
    print("API cliente: ", dados) #Conferir se o dado chegou
    resposta = processar_cliente('criar_cliente', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar clientes
@app.route('/cliente', methods=['GET'])
def listar_clientes():
    resposta = processar_cliente('listar_clientes')
    return jsonify(resposta)

# Rota para atualizar cliente
@app.route('/cliente/<int:idCliente>', methods=['PUT'])
def atualizar_cliente(idCliente):
    dados = request.json
    dados['idCliente'] = idCliente
    resposta = processar_cliente('atualizar_cliente', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir cliente
@app.route('/cliente/<int:idcliente>', methods=['DELETE'])
def deletar_cliente(idcliente):
    resposta = processar_cliente('excluir_cliente', {'idcliente': idcliente})
    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)
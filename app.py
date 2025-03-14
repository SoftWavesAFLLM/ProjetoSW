from flask import Flask, request, jsonify 
from processamento import processar_maquina, processar_usuario, processar_sensor, processar_odmanutencao, processar_trabalho_ordens, processar_peca

app = Flask(__name__)


#--------------------INICIO - Rota Maquinas --------------------

#Rota para criação de novas maquinas
@app.route('/maquina', methods=['POST'])
def criar_maquina():
    dados = request.json
    print("API maquina: ", dados) #Conferir se o dado chegou
    resposta = processar_maquina('criar_maquina', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar maquinas
@app.route('/maquina', methods=['GET'])
def listar_maquinas():
    resposta = processar_maquina('listar_maquinas')
    return jsonify(resposta)

# Rota para atualizar maquina
@app.route('/maquina/<int:idmaquinas>', methods=['PUT'])
def atualizar_maquina(idmaquinas):
    dados = request.json
    dados['idmaquinas'] = idmaquinas
    resposta = processar_maquina('atualizar_maquina', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir maquina
@app.route('/maquina/<int:idmaquinas>', methods=['DELETE'])
def deletar_maquina(idmaquinas):
    resposta = processar_maquina('excluir_maquina', {'idmaquinas': idmaquinas})
    return jsonify(resposta)

#--------------------FIM - Rota Maquinas--------------------



#--------------------INICIO - Rota Usuarios--------------------

#Rota para criação de novos usuarios
@app.route('/usuario', methods=['POST'])
def criar_usuario():
    dados = request.json
    print("API usuario: ", dados) #Conferir se o dado chegou
    resposta = processar_usuario('criar_usuario', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar usuarios
@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    resposta = processar_usuario('listar_usuarios')
    return jsonify(resposta)

# Rota para atualizar usuario
@app.route('/usuario/<int:idusuario>', methods=['PUT'])
def atualizar_usuario(idusuario):
    dados = request.json
    dados['idusuario'] = idusuario
    resposta = processar_usuario('atualizar_usuario', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir usuario
@app.route('/usuario/<int:idusuario>', methods=['DELETE'])
def deletar_usuario(idusuario):
    resposta = processar_usuario('excluir_usuario', {'idusuario': idusuario})
    return jsonify(resposta)

#--------------------FIM - Rota Usuarios--------------------



#----------------INICIO - Rota Sensores----------------

#Rota para criação de novos sensor
@app.route('/sensores', methods=['POST'])
def insert_sensor():
    dados = request.json
    print("API sensor: ", dados) #Conferir se o dado chegou
    resposta = processar_sensor('insert_sensor', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar sensores
@app.route('/sensores', methods=['GET'])
def read_sensor():
    resposta = processar_sensor('read_sensor')
    return jsonify(resposta)

# Rota para atualizar sensor
@app.route('/sensores/<int:idsensores>', methods=['PUT'])
def update_sensor(idsensores):
    dados = request.json
    dados['idsensores'] = idsensores
    resposta = processar_sensor('update_sensor', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir sensor
@app.route('/sensores/<int:idsensores>', methods=['DELETE'])
def delete_sensor(idsensores):
    resposta = processar_sensor('delete_sensor', {'idsensores': idsensores})
    return jsonify(resposta)

#----------------FIM - Rota Sensores----------------



#----------------INICIO - Rota Manutenção----------------

#Rota para criação de novas ordens de manutenção
@app.route('/manutencao', methods=['POST'])
def criar_odmanutencao():
    dados = request.json
    print("API manutencao: ", dados) #Conferir se o dado chegou
    resposta = processar_odmanutencao('criar_odmanutencao', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar ordem de manutenção
@app.route('/manutencao', methods=['GET'])
def listar_odmanutencao():
    resposta = processar_odmanutencao('listar_odmanutencao')
    return jsonify(resposta)

# Rota para atualizar ordem de manutenção
@app.route('/manutencao/<int:idordens_manutencao>', methods=['PUT'])
def atualizar_odmanutencao(idordens_manutencao):
    dados = request.json
    dados['idordens_manutencao'] = idordens_manutencao
    resposta = processar_odmanutencao('atualizar_odmanutencao', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir ordem de manutenção
@app.route('/manutencao/<int:idordens_manutencao>', methods=['DELETE'])
def deletar_odmanutencao(idordens_manutencao):
    resposta = processar_odmanutencao('excluir_odmanutencao', {'idordens_manutencao': idordens_manutencao})
    return jsonify(resposta)

#----------------FIM - Rota Manutenção----------------



#----------------INICIO - Rota Trabalho em Ordens----------------

#Rota para criação de novas trabalho em ordens
@app.route('/trabalho_ordens', methods=['POST'])
def criar_trabalho_ordens():
    dados = request.json
    print("API maquina: ", dados) #Conferir se o dado chegou
    resposta = processar_trabalho_ordens('criar_trabalho_ordens', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar trabalhos em ordens
@app.route('/trabalho_ordens', methods=['GET'])
def listar_trabalho_ordens():
    resposta = processar_trabalho_ordens('listar_trabalho_ordens')
    return jsonify(resposta)

# Rota para atualizar trabalho em ordem
@app.route('/trabalho_ordens/<int:idordens>', methods=['PUT'])
def atualizar_trabalho_ordens(idordens):
    dados = request.json
    dados['idordens'] = idordens
    resposta = processar_trabalho_ordens('atualizar_trabalho_ordens', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir trabalho em ordem
@app.route('/trabalho_ordens/<int:idordens>', methods=['DELETE'])
def deletar_trabalho_ordens(idordens):
    resposta = processar_trabalho_ordens('excluir_trabalho_ordens', {'idordens': idordens})
    return jsonify(resposta)

#----------------FIM - Rota Trabalho em Ordens----------------



#--------------------INICIO - Rota Peças --------------------

#Rota para criação de novas peças
@app.route('/peca', methods=['POST'])
def criar_peca():
    dados = request.json
    print("API pecas: ", dados) #Conferir se o dado chegou
    resposta = processar_peca('criar_peca', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar peças
@app.route('/peca', methods=['GET'])
def listar_pecas():
    resposta = processar_peca('listar_pecas')
    return jsonify(resposta)

# Rota para atualizar peças
@app.route('/peca/<int:idpecas>', methods=['PUT'])
def atualizar_peca(idpecas):
    dados = request.json
    dados['idpecas'] = idpecas
    resposta = processar_peca('atualizar_peca', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir peças
@app.route('/peca/<int:idpecas>', methods=['DELETE'])
def deletar_peca(idpecas):
    resposta = processar_peca('excluir_peca', {'idpecas': idpecas})
    return jsonify(resposta)

#--------------------FIM - Rota Peças--------------------


if __name__ == '__main__':
    app.run(debug=True)
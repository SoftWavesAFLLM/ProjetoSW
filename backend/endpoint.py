from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from processamento import processar_maquina, processar_usuario, processar_sensor, processar_odmanutencao, processar_trabalho_ordens, processar_peca, processar_DOM
from select_mono import generic_select
from select_multi import generic_join_select
from gestor_mqtt import mqtt_client

api_bp = Blueprint('api', __name__)


#--------------------INICIO - Rota Maquinas --------------------

#Rota para criação de novas maquinas
@api_bp.route('/api/maquina', methods=['POST'])
def criar_maquina():
    dados = request.json
    print("API maquina: ", dados) #Conferir se o dado chegou
    resposta = processar_maquina('criar_maquina', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar maquinas
@api_bp.route('/api/maquina', methods=['GET'])
def listar_maquinas():
    resposta = processar_maquina('listar_maquinas')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar maquina
@api_bp.route('/api/maquina/<int:idmaquinas>', methods=['PUT'])
def atualizar_maquina(idmaquinas):
    dados = request.json
    dados['idmaquinas'] = idmaquinas
    resposta = processar_maquina('atualizar_maquina', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir maquina
@api_bp.route('/api/maquina/<int:idmaquinas>', methods=['DELETE'])
def deletar_maquina(idmaquinas):
    resposta = processar_maquina('excluir_maquina', {'idmaquinas': idmaquinas})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#--------------------FIM - Rota Maquinas--------------------



#--------------------INICIO - Rota Usuarios--------------------

#Rota para criação de novos usuarios
@api_bp.route('/api/usuario', methods=['POST'])
def criar_usuario():
    dados = request.json
    print("API usuario: ", dados) #Conferir se o dado chegou
    if 'senha' in dados:
        dados['senha'] = generate_password_hash(dados['senha'])
    resposta = processar_usuario('criar_usuario', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar usuarios
@api_bp.route('/api/usuario', methods=['GET'])
def listar_usuarios():
    resposta = processar_usuario('listar_usuarios')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar usuario
@api_bp.route('/api/usuario/<int:idusuario>', methods=['PUT'])
def atualizar_usuario(idusuario):
    dados = request.json
    dados['idusuario'] = idusuario
    resposta = processar_usuario('atualizar_usuario', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir usuario
@api_bp.route('/api/usuario/<int:idusuario>', methods=['DELETE'])
def deletar_usuario(idusuario):
    resposta = processar_usuario('excluir_usuario', {'idusuario': idusuario})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#--------------------FIM - Rota Usuarios--------------------



#----------------INICIO - Rota Sensores----------------

#Rota para criação de novos sensor
@api_bp.route('/api/sensores', methods=['POST'])
def insert_sensor():
    dados = request.json
    print("API sensor: ", dados) #Conferir se o dado chegou
    resposta = processar_sensor('insert_sensor', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar sensores
@api_bp.route('/api/sensores', methods=['GET'])
def read_sensor():
    resposta = processar_sensor('read_sensor')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar sensor
@api_bp.route('/api/sensores/<int:idsensores>', methods=['PUT'])
def update_sensor(idsensores):
    dados = request.json
    dados['idsensores'] = idsensores
    resposta = processar_sensor('update_sensor', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir sensor
@api_bp.route('/api/sensores/<int:idsensores>', methods=['DELETE'])
def delete_sensor(idsensores):
    resposta = processar_sensor('delete_sensor', {'idsensores': idsensores})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#----------------FIM - Rota Sensores----------------



#----------------INICIO - Rota Manutenção----------------

#Rota para criação de novas ordens de manutenção
@api_bp.route('/api/manutencao', methods=['POST'])
def criar_odmanutencao():
    dados = request.json
    print("API manutencao: ", dados) #Conferir se o dado chegou
    resposta = processar_odmanutencao('criar_odmanutencao', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar ordem de manutenção
@api_bp.route('/api/manutencao', methods=['GET'])
def listar_odmanutencao():
    resposta = processar_odmanutencao('listar_odmanutencao')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar ordem de manutenção
@api_bp.route('/api/manutencao/<int:idordens_manutencao>', methods=['PUT'])
def atualizar_odmanutencao(idordens_manutencao):
    dados = request.json
    dados['idordens_manutencao'] = idordens_manutencao
    resposta = processar_odmanutencao('atualizar_odmanutencao', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir ordem de manutenção
@api_bp.route('/api/manutencao/<int:idordens_manutencao>', methods=['DELETE'])
def deletar_odmanutencao(idordens_manutencao):
    resposta = processar_odmanutencao('excluir_odmanutencao', {'idordens_manutencao': idordens_manutencao})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#----------------FIM - Rota Manutenção----------------



#----------------INICIO - Rota Trabalho em Ordens----------------

#Rota para criação de novas trabalho em ordens
@api_bp.route('/api/trabalho_ordens', methods=['POST'])
def criar_trabalho_ordens():
    dados = request.json
    print("API maquina: ", dados) #Conferir se o dado chegou
    resposta = processar_trabalho_ordens('criar_trabalho_ordens', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar trabalhos em ordens
@api_bp.route('/api/trabalho_ordens', methods=['GET'])
def listar_trabalho_ordens():
    resposta = processar_trabalho_ordens('listar_trabalho_ordens')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar trabalho em ordem
@api_bp.route('/api/trabalho_ordens/<int:idordens>', methods=['PUT'])
def atualizar_trabalho_ordens(idordens):
    dados = request.json
    dados['idordens'] = idordens
    resposta = processar_trabalho_ordens('atualizar_trabalho_ordens', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir trabalho em ordem
@api_bp.route('/api/trabalho_ordens/<int:idordens>', methods=['DELETE'])
def deletar_trabalho_ordens(idordens):
    resposta = processar_trabalho_ordens('excluir_trabalho_ordens', {'idordens': idordens})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#----------------FIM - Rota Trabalho em Ordens----------------



#--------------------INICIO - Rota Peças --------------------

#Rota para criação de novas peças
@api_bp.route('/api/peca', methods=['POST'])
def criar_peca():
    dados = request.json
    print("API pecas: ", dados) #Conferir se o dado chegou
    resposta = processar_peca('criar_peca', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar peças
@api_bp.route('/api/peca', methods=['GET'])
def listar_pecas():
    resposta = processar_peca('listar_pecas')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar peças
@api_bp.route('/api/peca/<int:idpecas>', methods=['PUT'])
def atualizar_peca(idpecas):
    dados = request.json
    dados['idpecas'] = idpecas
    resposta = processar_peca('atualizar_peca', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir peças
@api_bp.route('/api/peca/<int:idpecas>', methods=['DELETE'])
def deletar_peca(idpecas):
    resposta = processar_peca('excluir_peca', {'idpecas': idpecas})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#--------------------FIM - Rota Peças--------------------



#--------------------INICIO - Rota Detalhes da ordem de manutenção --------------------

#Rota para criação de novas DOM
@api_bp.route('/api/DOM', methods=['POST'])
def criar_DOM():
    dados = request.json
    print("API DOM: ", dados) #Conferir se o dado chegou
    resposta = processar_DOM('criar_DOM', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#Rota para listar DOMs
@api_bp.route('/api/DOM', methods=['GET'])
def listar_DOMs():
    resposta = processar_DOM('listar_DOMs')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar DOM
@api_bp.route('/api/DOM/<int:iddetalhes_ordens_manutencao>', methods=['PUT'])
def atualizar_DOM(iddetalhes_ordens_manutencao):
    dados = request.json
    dados['iddetalhes_ordens_manutencao'] = iddetalhes_ordens_manutencao
    resposta = processar_DOM('atualizar_DOM', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

#Rota para excluir DOM
@api_bp.route('/api/DOM/<int:iddetalhes_ordens_manutencao>', methods=['DELETE'])
def deletar_DOM(iddetalhes_ordens_manutencao):
    resposta = processar_DOM('excluir_DOM', {'iddetalhes_ordens_manutencao': iddetalhes_ordens_manutencao})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

#--------------------FIM - Rota Detalhes da ordem de manutenção--------------------



#--------------------INICIO - Rota Select--------------------

@api_bp.route("/api/generic_select", methods=["POST"])
def api_generic_select():
    data = request.get_json()
    table = data.get("table")
    columns = data.get("columns", "*")
    where = data.get("where")
    order_by = data.get("order_by")
    limit = data.get("limit")
    database = data.get("database", "base")
   
    # Chama a função genérica de select
    result = generic_select(table, columns, where, order_by, limit, database)
    return jsonify(result)

@api_bp.route("/api/join_select", methods=["POST"])
def api_join_select():
    data = request.get_json()
    main_table = data.get("main_table")
    joins = data.get("joins", [])
    columns = data.get("columns", "*")
    where = data.get("where")
    order_by = data.get("order_by")
    limit = data.get("limit")
    database = data.get("database", "base")
   
    # Chama a função genérica para select com JOINs
    result = generic_join_select(main_table, joins, columns, where, order_by, limit, database)
    return jsonify(result)

#--------------------FIM - Rota Select--------------------



#-------------------EXEMPLO DE PUBLICAÇÃO MQTT----------------- 

@api_bp.route('/api/mqtt/publish', methods=['POST'])
def publish_mqtt():
    """
    Publica em qualquer tópico MQTT via JSON:
    { "topic": "sensores/temperatura", "payload": "25.3" }
    """
    body  = request.json or {}
    topic = body.get('topic')
    data  = body.get('payload', '')
    mqtt_client.publish(topic, data)
    return jsonify({
        'status':  'publicado',
        'topic':   topic,
        'payload': data
    })
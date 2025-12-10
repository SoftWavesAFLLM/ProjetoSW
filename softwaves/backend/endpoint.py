from flask import Blueprint, request, jsonify
from conectar import get_connection
from sanitizacao import sanitizar
from werkzeug.security import check_password_hash
import mysql.connector
from processamento import processar_maquina, processar_usuario, processar_sensor, processar_odmanutencao, processar_trabalho_ordens, processar_peca, processar_DOM
from select_mono import generic_select
from select_multi import generic_join_select
from gestor_mqtt import mqtt_client
import psensor
import json
from datetime import datetime
import base64


api_bp = Blueprint('api', __name__)


"""
# --------------------INICIO - Rota Sensores Raspiberry--------------------


@api_bp.route("/api/sensores", methods=["GET"])
def listar():
    sensores = psensor.listar_sensores()
    leituras_formatadas = []
    if sensores:
        for leitura in sensores:
            valor = leitura.get('valor')
            valor_dict = None

            # Tenta transformar em dict
            if isinstance(valor, dict):
                valor_dict = valor
            elif isinstance(valor, str):
                try:
                    # Primeiro decode
                    valor_dict = json.loads(valor)
                    # Se ainda for string, decodifica de novo
                    if isinstance(valor_dict, str):
                        valor_dict = json.loads(valor_dict)
                except Exception as e:
                    print(f"[AVISO] Ignorando leitura inválida: {valor} ({e})")
                    continue
            else:
                print(f"[AVISO] Tipo inesperado: {type(valor)}. Pulando.")
                continue

            # Timestamp
            ts = leitura.get('data_hora')
            timestamp = ts.strftime('%Y-%m-%d %H:%M:%S') if ts else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Adiciona todos os tipos, ignorando timestamp
            for tipo, v in valor_dict.items():
                if tipo == 'timestamp':
                    continue
                leituras_formatadas.append({
                    "tipo": tipo,
                    "valor": v,
                    "timestamp": timestamp
                })

    print(f"Enviando {len(leituras_formatadas)} registros formatados para o dashboard.")
    return jsonify(leituras_formatadas)


# --------------------FIM - Rota Sensores Raspiberry--------------------
"""


# --------------------INICIO - Rota Login--------------------
# Endpoint para login

@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    senha = data.get('senha')
    print("JSON recebido:", data)

    if not email or not senha:
        return jsonify({'success': False, 'error': 'Email e senha são obrigatórios.'}), 400

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    if user is None:
        return jsonify({'success': False, 'error': 'Usuário não encontrado.'}), 404

    if not check_password_hash(user['senha'], senha):
        return jsonify({'success': False, 'error': 'Senha incorreta.'}), 401

    return jsonify({
        'success': True,
        'message': 'Login realizado com sucesso!',
        'usuario': {
            'id': user['idusuario'],
            'nome': user['nome_usuario'],
            'email': user['email']
        }
    }), 200
# --------------------FIM - Rota Login--------------------


# --------------------INICIO - Rota Maquinas--------------------
# Rota para listar maquinas
@api_bp.route('/api/maquina', methods=['POST'])
def insert_maquina():
    dados = sanitizar(request.json)
    print("📥 Dados recebidos no endpoint /api/maquina:", dados)

    # A imagem virá em dados['imagem'] (completo, incluindo prefixo)
    imagem_base64 = dados.get('imagem')

    if imagem_base64:
        print("📷 Base64 recebido (10 chars):", imagem_base64[:10])
        print("📏 Tamanho total do Base64:", len(imagem_base64))

        # Remove o prefixo "data:image/jpeg;base64,"
        if ',' in imagem_base64:
            imagem_base64 = imagem_base64.split(',', 1)[1]

        try:
            imagem_bytes = base64.b64decode(imagem_base64)
            dados['imagem'] = imagem_bytes  # salva como bytes reais
            print("✅ Imagem decodificada com sucesso. Bytes:", len(imagem_bytes))

        except Exception as e:
            print("❌ Erro ao decodificar a imagem:", e)
            return jsonify({
                'status': 'erro',
                'mensagem': 'Erro ao decodificar a imagem'
            }), 400

    else:
        print("⚠️ Nenhuma imagem recebida")
        dados['imagem'] = None

    # *** PROCESSAMENTO ***
    print("dados inserir", dados)
    resposta = processar_maquina('criar_maquina', dados)
    
    status_code = 201 if resposta.get('status') == 'sucesso' else 400
    
    return jsonify(resposta), status_code



@api_bp.route('/api/maquina', methods=['GET'])
def listar_maquinas():
    resposta = processar_maquina('listar_maquinas')
    return jsonify(resposta), 200

# Rota para atualizar maquina


@api_bp.route('/api/maquina/<int:idmaquinas>', methods=['PUT'])
def atualizar_maquina(idmaquinas):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idmaquinas'] = idmaquinas
    resposta = processar_maquina('atualizar_maquina', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir maquina


@api_bp.route('/api/maquina/<int:idmaquinas>', methods=['DELETE'])
def deletar_maquina(idmaquinas):
    resposta = processar_maquina('excluir_maquina', {'idmaquinas': idmaquinas})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# --------------------FIM - Rota Maquinas--------------------


# --------------------INICIO - Rota Usuarios--------------------

# Rota para criação de novos usuarios
@api_bp.route('/api/usuario', methods=['POST'])
def criar_usuario():
    dados_ns = request.json
    print("API usuario: ", dados_ns)  # Conferir se o dado chegou
    # Sanitiza os dados para evitar possíveis problemas
    dados = sanitizar(dados_ns)
    resposta = processar_usuario('criar_usuario', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para listar usuarios


@api_bp.route('/api/usuario', methods=['GET'])
def listar_usuarios():
    resposta = processar_usuario('listar_usuarios')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar usuario


@api_bp.route('/api/usuario/<int:idusuario>', methods=['PUT'])
def atualizar_usuario(idusuario):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idusuario'] = idusuario
    resposta = processar_usuario('atualizar_usuario', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir usuario


@api_bp.route('/api/usuario/<int:idusuario>', methods=['DELETE'])
def deletar_usuario(idusuario):
    resposta = processar_usuario('excluir_usuario', {'idusuario': idusuario})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# --------------------FIM - Rota Usuarios--------------------


# ----------------INICIO - Rota Sensores----------------

# Rota para criação de novos sensor
@api_bp.route('/api/sensor', methods=['POST'])
def insert_sensor():
    dados = sanitizar(request.json)
    print("API sensor: ", dados)

    imagem_base64 = dados.get('imagem')
    if imagem_base64:
        print("📷 Base64 recebido (10 chars):", imagem_base64[:10])
        print("📏 Tamanho total do Base64:", len(imagem_base64))

        if ',' in imagem_base64:
            imagem_base64 = imagem_base64.split(',', 1)[1]

        try:
            imagem_bytes = base64.b64decode(imagem_base64)
            dados['imagem'] = imagem_bytes
            print("✅ Imagem decodificada com sucesso. Bytes:", len(imagem_bytes))

        except Exception as e:
            print("❌ Erro ao decodificar a imagem:", e)
            return jsonify({
                'status': 'erro',
                'mensagem': 'Erro ao decodificar a imagem'
            }), 400
    else:
        print("⚠️ Nenhuma imagem recebida")
        dados['imagem'] = None

    # *** PROCESSAMENTO ***
    print("dados inserir", dados)
    resposta = processar_sensor('insert_sensor', dados)  # <-- CORRIGIDO

    status_code = 201 if resposta.get('status') == 'sucesso' else 400
    return jsonify(resposta), status_code

# Rota para listar sensores


@api_bp.route('/api/sensor', methods=['GET'])
def read_sensor():
    resposta = processar_sensor('read_sensor')
    print('Dados Consultados', resposta)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar sensor


@api_bp.route('/api/sensor/<int:idsensores>', methods=['PUT'])
def update_sensor(idsensores):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idsensores'] = idsensores
    resposta = processar_sensor('update_sensor', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir sensor


@api_bp.route('/api/sensor/<int:idsensores>', methods=['DELETE'])
def delete_sensor(idsensores):
    resposta = processar_sensor('delete_sensor', {'idsensores': idsensores})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# ----------------FIM - Rota Sensores----------------


# ----------------INICIO - Rota Manutenção----------------

# Rota para criação de novas ordens de manutenção
@api_bp.route('/api/manutencao', methods=['POST'])
def criar_odmanutencao():
    dados_ns = request.json
    print("API manutencao: ", dados_ns)  # Conferir se o dado chegou
    dados = sanitizar(dados_ns)
    resposta = processar_odmanutencao('criar_odmanutencao', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para listar ordem de manutenção


@api_bp.route('/api/manutencao', methods=['GET'])
def listar_odmanutencao():
    resposta = processar_odmanutencao('listar_odmanutencao')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar ordem de manutenção


@api_bp.route('/api/manutencao/<int:idordens_manutencao>', methods=['PUT'])
def atualizar_odmanutencao(idordens_manutencao):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idordens_manutencao'] = idordens_manutencao
    resposta = processar_odmanutencao('atualizar_odmanutencao', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir ordem de manutenção


@api_bp.route('/api/manutencao/<int:idordens_manutencao>', methods=['DELETE'])
def deletar_odmanutencao(idordens_manutencao):
    resposta = processar_odmanutencao(
        'excluir_odmanutencao', {'idordens_manutencao': idordens_manutencao})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# ----------------FIM - Rota Manutenção----------------


# ----------------INICIO - Rota Trabalho em Ordens----------------

# Rota para criação de novas trabalho em ordens
@api_bp.route('/api/trabalho_ordens', methods=['POST'])
def criar_trabalho_ordens():
    dados_ns = request.json
    print("API maquina: ", dados_ns)  # Conferir se o dado chegou
    dados = sanitizar(dados_ns)
    resposta = processar_trabalho_ordens('criar_trabalho_ordens', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para listar trabalhos em ordens


@api_bp.route('/api/trabalho_ordens', methods=['GET'])
def listar_trabalho_ordens():
    resposta = processar_trabalho_ordens('listar_trabalho_ordens')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar trabalho em ordem


@api_bp.route('/api/trabalho_ordens/<int:idordens>', methods=['PUT'])
def atualizar_trabalho_ordens(idordens):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idordens'] = idordens
    resposta = processar_trabalho_ordens('atualizar_trabalho_ordens', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir trabalho em ordem


@api_bp.route('/api/trabalho_ordens/<int:idordens>', methods=['DELETE'])
def deletar_trabalho_ordens(idordens):
    resposta = processar_trabalho_ordens(
        'excluir_trabalho_ordens', {'idordens': idordens})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# ----------------FIM - Rota Trabalho em Ordens----------------


# --------------------INICIO - Rota Peças --------------------

# Rota para criação de novas peças
@api_bp.route('/api/peca', methods=['POST'])
def criar_peca():
    dados_ns = request.json
    print("API pecas: ", dados_ns)  # Conferir se o dado chegou
    dados = sanitizar(dados_ns)
    resposta = processar_peca('criar_peca', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para listar peças


@api_bp.route('/api/peca', methods=['GET'])
def listar_pecas():
    resposta = processar_peca('listar_pecas')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar peças


@api_bp.route('/api/peca/<int:idpecas>', methods=['PUT'])
def atualizar_peca(idpecas):
    dados_ns = request.json
    dados = sanitizar(dados_ns)
    dados['idpecas'] = idpecas
    resposta = processar_peca('atualizar_peca', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir peças


@api_bp.route('/api/peca/<int:idpecas>', methods=['DELETE'])
def deletar_peca(idpecas):
    resposta = processar_peca('excluir_peca', {'idpecas': idpecas})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# --------------------FIM - Rota Peças--------------------


# --------------------INICIO - Rota Detalhes da ordem de manutenção --------------------

# Rota para criação de novas DOM
@api_bp.route('/api/DOM', methods=['POST'])
def criar_DOM():
    dados = request.json
    print("API DOM: ", dados)  # Conferir se o dado chegou
    resposta = processar_DOM('criar_DOM', dados)
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para listar DOMs


@api_bp.route('/api/DOM', methods=['GET'])
def listar_DOMs():
    resposta = processar_DOM('listar_DOMs')
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# Rota para atualizar DOM


@api_bp.route('/api/DOM/<int:iddetalhes_ordens_manutencao>', methods=['PUT'])
def atualizar_DOM(iddetalhes_ordens_manutencao):
    dados = request.json
    dados = sanitizar(dados)
    dados['iddetalhes_ordens_manutencao'] = iddetalhes_ordens_manutencao
    resposta = processar_DOM('atualizar_DOM', dados)
    return jsonify(resposta), 200 if resposta.get('status') == 'sucesso' else 400

# Rota para excluir DOM


@api_bp.route('/api/DOM/<int:iddetalhes_ordens_manutencao>', methods=['DELETE'])
def deletar_DOM(iddetalhes_ordens_manutencao):
    resposta = processar_DOM(
        'excluir_DOM', {'iddetalhes_ordens_manutencao': iddetalhes_ordens_manutencao})
    return jsonify(resposta), 201 if resposta.get('status') == 'sucesso' else 400

# --------------------FIM - Rota Detalhes da ordem de manutenção--------------------


# --------------------INICIO - Rota Select--------------------

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
    result = generic_join_select(
        main_table, joins, columns, where, order_by, limit, database)
    return jsonify(result)

# --------------------FIM - Rota Select--------------------


# -------------------EXEMPLO DE PUBLICAÇÃO MQTT-----------------

@api_bp.route('/api/mqtt/publish', methods=['POST'])
def publish_mqtt():
    """
    Publica em qualquer tópico MQTT via JSON:
    { "topic": "sensores/temperatura", "payload": "25.3" }
    """
    body = request.json or {}
    topic = body.get('topic')
    data = body.get('payload', '')
    mqtt_client.publish(topic, data)
    print('body', body)
    return jsonify({
        'status':  'publicado',
        'topic':   topic,
        'payload': data
    })

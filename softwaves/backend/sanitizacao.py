from markupsafe import escape

def sanitizar(dados_ns):
    print("➡️ Entrada recebida para sanitização:")
    print(dados_ns)

    dados = {}

    # ---------------------- MÁQUINA ----------------------
    campos_texto_maquina = [
        'nome_maquina', 'localizacao', 'status_maquina', 'fabricante'
    ]

    for campo in campos_texto_maquina:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    if 'data_instalacao_maquina' in dados_ns:
        dados['data_instalacao_maquina'] = dados_ns.get('data_instalacao_maquina')

    # ---------------------- IMAGEM ----------------------
    # Aceita imagem OU imagemBase64, mantém íntegra no banco
    imagem_b64 = None

    if 'imagem' in dados_ns:
        imagem_b64 = dados_ns.get('imagem')

    elif 'imagemBase64' in dados_ns:
        imagem_b64 = dados_ns.get('imagemBase64')

    if imagem_b64:
        dados['imagem'] = imagem_b64
        print(f"📷 Imagem recebida - tamanho total: {len(imagem_b64)}")
        print("📷 Base64 (10 primeiros chars):", imagem_b64[:10])

    # ---------------------- USUÁRIO ----------------------
    campos_texto_usuario = ['nome_usuario', 'email', 'telefone', 'cargo']
    for campo in campos_texto_usuario:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    if 'senha' in dados_ns:
        dados['senha'] = dados_ns.get('senha')

    if 'cpf_cnpj' in dados_ns:
        dados['cpf_cnpj'] = dados_ns.get('cpf_cnpj')

    # ---------------------- SENSOR ----------------------
    campos_texto_sensor = ['tipo_sensor', 'descricao_sensor']
    for campo in campos_texto_sensor:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    if 'data_instalacao_sensor' in dados_ns:
        dados['data_instalacao_sensor'] = dados_ns.get('data_instalacao_sensor')

    if 'maquinas_idmaquinas' in dados_ns:
        dados['maquinas_idmaquinas'] = dados_ns.get('maquinas_idmaquinas')

    # ---------------------- MANUTENÇÃO ----------------------
    campos_texto_manut = ['descricao_problema', 'status_manutencao', 'tipo_manutencao']
    for campo in campos_texto_manut:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    if 'usuario_idusuario' in dados_ns:
        dados['usuario_idusuario'] = dados_ns.get('usuario_idusuario')

    if 'maquinas_idmaquinas' in dados_ns:
        dados['maquinas_idmaquinas'] = dados_ns.get('maquinas_idmaquinas')

    # ---------------------- ORDENS ----------------------
    campos_texto_ordem = ['descricao_manutencao', 'status_ordem']
    for campo in campos_texto_ordem:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    datas_ordem = ['data_criacao', 'data_conclusao']
    for campo in datas_ordem:
        if campo in dados_ns:
            dados[campo] = dados_ns.get(campo)

    if 'ordens_manutencao_idordens_manutencao' in dados_ns:
        dados['ordens_manutencao_idordens_manutencao'] = dados_ns.get('ordens_manutencao_idordens_manutencao')

    if 'usuarios_idusuario' in dados_ns:
        dados['usuarios_idusuario'] = dados_ns.get('usuarios_idusuario')

    # ---------------------- PEÇAS ----------------------
    campos_texto_peca = ['nome_pecas', 'codigo_pecas', 'quantidade']
    for campo in campos_texto_peca:
        if campo in dados_ns:
            valor = dados_ns.get(campo)
            dados[campo] = str(escape(valor.strip())) if valor else None

    print("✔️ Dados finalizados para inserção:")
    print(dados)
    print("--------------------------------------------------------------")

    return dados

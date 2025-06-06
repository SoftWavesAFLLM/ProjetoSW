from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re
from markupsafe import escape

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',      # altere para o seu usuário
        password='root',    # altere para a sua senha
        database='base'     # altere para o seu banco de dados
    )
    return connection

# Função para validar o formato de email usando regex
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Função para validar os dados de cadastro
def validate_register_data(data):
    errors = []
    
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    telefone = data.get('telefone')
    cargo = data.get('cargo')
    
    if not nome or not nome.strip():
        errors.append("Nome é obrigatório.")
    elif len(nome) > 100:
        errors.append("Nome excede o tamanho máximo de 100 caracteres.")
    
    if not email or not email.strip():
        errors.append("Email é obrigatório.")
    elif not is_valid_email(email):
        errors.append("Email inválido.")
    elif len(email) > 100:
        errors.append("Email excede o tamanho máximo de 100 caracteres.")
        
    if not senha:
        errors.append("Senha é obrigatória.")
        
    if telefone:
        if len(telefone) > 20:
            errors.append("Telefone excede o tamanho máximo de 20 caracteres.")
        # Validação para permitir apenas dígitos e alguns caracteres comuns em telefones
        if not re.match(r'^[0-9\-\+\(\)\s]*$', telefone):
            errors.append("Telefone contém caracteres inválidos.")
    
    if cargo and len(cargo) > 50:
        errors.append("Cargo excede o tamanho máximo de 50 caracteres.")
    
    return errors

# Endpoint para cadastro de usuário com validação e sanitização
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Valida os dados recebidos
    errors = validate_register_data(data)
    if errors:
        return jsonify({'errors': errors}), 400
    
    # Sanitiza os dados para evitar possíveis problemas
    nome = escape(data.get('nome').strip())
    email = escape(data.get('email').strip())
    senha = data.get('senha')
    telefone = escape(data.get('telefone').strip()) if data.get('telefone') else None
    cargo = escape(data.get('cargo').strip()) if data.get('cargo') else None

    # Criptografa a senha
    senha_hash = generate_password_hash(senha)
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO usuario (nome, email, telefone, cargo, senha) VALUES (%s, %s, %s, %s, %s)",
            (nome, email, telefone, cargo, senha_hash)
        )
        connection.commit()
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()
    
    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'error': 'Email e senha são obrigatórios.'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    if user is None:
        return jsonify({'error': 'Usuário não encontrado.'}), 404

    # Verifica se a senha informada corresponde ao hash armazenado
    if not check_password_hash(user['senha'], senha):
        return jsonify({'error': 'Senha incorreta.'}), 401

    return jsonify({'message': 'Login realizado com sucesso!'}), 200

if __name__ == '__main__':
    app.run(debug=True)

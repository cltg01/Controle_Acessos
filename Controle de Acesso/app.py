import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.utils import secure_filename
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, LargeBinary, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Chave secreta para gerenciar a sessão

# Configuração do banco de dados MySQL
db_user = os.getenv('DB_USER', 'teste')
db_password = os.getenv('DB_PASSWORD', 'ligacoesGD9')
db_name = os.getenv('DB_NAME', 'sistema')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')

db_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Definição das tabelas
class Usuario(Base):
    __tablename__ = 'tabela_usuario'
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nome_usuario = Column(String(50), nullable=False, unique=True)
    email_usuario = Column(String(50))
    senha_usuario = Column(String(255), nullable=False)

class Credenciado(Base):
    __tablename__ = 'tabela_credenciado'
    id_credenciado = Column(Integer, primary_key=True, autoincrement=True)
    nome_credenciado = Column(String(50), nullable=False)
    cpf_credenciado = Column(String(11), unique=True, nullable=False)
    telefone_credenciado = Column(String(20))
    email_credenciado = Column(String(50))
    tipo_credenciado = Column(Enum('Fornecedor', 'Cliente', 'Prestador de Serviço', 'Terceirizado', 'Liderança', 'Outro'), nullable=False)
    empresa_organizacao = Column(String(50))
    foto_credenciado = Column(LargeBinary)
    observacoes_credenciado = Column(Text)

class Acesso(Base):
    __tablename__ = 'tabela_acesso'
    id_acesso = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('tabela_usuario.id_usuario'))
    id_credenciado = Column(Integer, ForeignKey('tabela_credenciado.id_credenciado'))
    motivo_acesso = Column(Text)
    data_hora_entrada = Column(DateTime, nullable=False)
    data_hora_saida = Column(DateTime)
    status_acesso = Column(Enum('Em andamento', 'Concluído', 'Cancelado'), default='Em andamento')

Base.metadata.create_all(engine)

# Login Obrigatório
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('inicio', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Página de Login
@app.route('/')
def inicio():
    return render_template('login.html')

# Implementação de Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nome_usuario = data.get('nome_usuario')
    senha_usuario = data.get('senha_usuario')

    if not nome_usuario or not senha_usuario:
        return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

    session_db = Session()
    try:
        user = session_db.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
    except SQLAlchemyError:
        return jsonify({'message': 'Erro ao acessar o banco de dados!'}), 500
    finally:
        session_db.close()

    if user and check_password_hash(user.senha_usuario, senha_usuario):
        session['logged_in'] = True
        session['nome_usuario'] = nome_usuario  # Armazenar o nome do usuário na sessão
        
        # Redireciona para a página de administrador se o usuário for "ADMIN"
        if nome_usuario == "ADMIN":
            return jsonify({'message': 'Login realizado com sucesso!', 'redirect_url': url_for('home_admin')}), 200
        
        return jsonify({'message': 'Login realizado com sucesso!', 'redirect_url': url_for('home')}), 200
    else:
        return jsonify({'message': 'Nome de usuário ou senha incorretos!'}), 401

# Rota de Logout
@app.route('/logout')
def logout():
    session.clear()  # Limpa todas as chaves da sessão
    return redirect(url_for('inicio'))

# Registro de Usuários
@app.route('/register', methods=['GET', 'POST'])

def register():
    if request.method == 'GET':
        try:
            with engine.connect() as conn:
                # Query para obter a lista de usuários
                query_lista_usuarios = """
                SELECT nome_usuario
                FROM tabela_usuario
                """
                result = conn.execute(query_lista_usuarios)
                usuarios = [row[0] for row in result]

        except Exception as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            usuarios = []

        # Renderizar o template com a lista de usuários
        return render_template('register.html', usuarios=usuarios)
    
    # Implementação de registro de novos usuários
    elif request.method == 'POST':
        data = request.get_json()
        nome_usuario = data.get('nome_usuario')
        senha_usuario = data.get('senha_usuario')

        if not nome_usuario or not senha_usuario:
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

        if not nome_usuario.isalnum():  # Permite apenas alfanuméricos
            return jsonify({'message': 'Nome de usuário deve conter apenas letras e números!'}), 400

        hashed_password = generate_password_hash(senha_usuario)

        session_db = Session()
        try:
            existing_user = session_db.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
            if existing_user:
                return jsonify({'message': 'Nome de usuário já existe!'}), 400

            new_user = Usuario(nome_usuario=nome_usuario, senha_usuario=hashed_password)
            session_db.add(new_user)
            session_db.commit()
            return jsonify({'message': 'Usuário criado com sucesso!', 'redirect_url': url_for('register')}), 201

        except SQLAlchemyError as e:
            session_db.rollback()
            return jsonify({'message': f'Erro ao registrar usuário: {str(e)}'}), 500
        finally:
            session_db.close()

# Página de Administração
@app.route('/home_admin')
@login_required
def home_admin():
    nome_usuario_logado = session.get('nome_usuario')  # Recuperar o nome do usuário da sessão
    if not nome_usuario_logado:
        return redirect(url_for('inicio'))  # Redirecionar para login se não houver usuário logado

    return render_template('home_admin.html')

# Página de Usuário Comum
@app.route('/home')
@login_required
def home():
    nome_usuario_logado = session.get('nome_usuario')  # Recuperar o nome do usuário da sessão
    if not nome_usuario_logado:
        return redirect(url_for('inicio'))  # Redirecionar para login se não houver usuário logado

    return render_template('home.html') 

# Cadastro de credenciado
@app.route('/cadastro_credenciado', methods=['GET', 'POST'])
@login_required
def cadastro_credenciado():
    if request.method == 'GET':
        return render_template('cadastro_credenciado.html')

    elif request.method == 'POST':
        data = request.get_json()
        nome_credenciado = data.get('nome_credenciado')
        cpf_credenciado = data.get('cpf_credenciado')
        telefone_credenciado = data.get('telefone_credenciado')
        email_credenciado = data.get('email_credenciado')
        tipo_credenciado = data.get('tipo_credenciado')
        empresa_organizacao = data.get('empresa_organizacao')
        observacoes_credenciado = data.get('observacoes_credenciado')

        # Validações
        if not nome_credenciado or not cpf_credenciado or not tipo_credenciado:
            return jsonify({'message': 'Nome, CPF e Tipo são obrigatórios!'}), 400

        session_db = Session()
        try:
            new_credenciado = Credenciado(
                nome_credenciado=nome_credenciado,
                cpf_credenciado=cpf_credenciado,
                telefone_credenciado=telefone_credenciado,
                email_credenciado=email_credenciado,
                tipo_credenciado=tipo_credenciado,
                empresa_organizacao=empresa_organizacao,
                observacoes_credenciado=observacoes_credenciado
            )
            session_db.add(new_credenciado)
            session_db.commit()
            return jsonify({'message': 'Credenciado cadastrado com sucesso!', 'redirect_url': url_for('cadastro_credenciado')}), 201

        except SQLAlchemyError as e:
            session_db.rollback()
            return jsonify({'message': f'Erro ao cadastrar credenciado: {str(e)}'}), 500
        finally:
            session_db.close()

if __name__ == '__main__':
    app.run(debug=True)
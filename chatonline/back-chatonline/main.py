from flask import Flask, request, jsonify 
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate(
    r"C:\Users\henri\OneDrive\Documentos\projetos\chatonline\back-chatonline\chatonline.json"
    )
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://chatonline-1c2cf-default-rtdb.firebaseio.com/'
})

def login(nome, senha):
    ref = db.reference(f'usuarios/{nome}')
    dados = ref.get()
    if dados and dados['senha'] == senha:
        print(f"Login bem-sucedido: {nome}")
        return True
    print("Nome ou senha incorretos!")
    return False

def cadastrar(nome, senha):
    ref = db.reference(f'usuarios/{nome}')
    if ref.get():  
        print("Usuário já existe!")
        return False
    ref.set({'senha': senha})
    print(f" Usuário {nome} cadastrado!")
    return True

@app.route('/login', methods=['POST'])
def rota_login():
    dados = request.get_json()
    nome = dados.get('nome')
    senha = dados.get('senha')

    if login(nome, senha):
        return jsonify({'success': True})
    return jsonify({'success': False})


@app.route('/cadastro', methods=['POST'])
def rota_cadastro():
    dados = request.get_json()
    nome = dados.get('nome')
    senha = dados.get('senha')

    if cadastrar(nome, senha):
        return jsonify({'success': True})
    return jsonify({'success': False, 'erro': 'Usuário já existe!'})


if __name__ == '__main__':
    app.run(debug=True)

app.py

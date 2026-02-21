from flask import Flask, request, jsonify
import json
import os
from cryptography.fernet import Fernet
from datetime import datetime

app = Flask(__name__)

# Carrega a mesma chave do sistema principal
def carregar_chave():
    return open("secret.key", "rb").read()

cipher_suite = Fernet(carregar_chave())
DB_FILE = "pilotos_encrypted.db"

@app.route('/registrar', methods=['POST'])
def registrar_global():
    try:
        dados_web = request.json
        # Blindagem imediata antes de salvar
        cripto = cipher_suite.encrypt(json.dumps(dados_web).encode())
        
        with open(DB_FILE, "ab") as f:
            f.write(cripto + b"\n")
            
        return jsonify({"status": "SUCESSO", "msg": "Piloto Autenticado no Flying Fortress"}), 200
    except Exception as e:
        return jsonify({"status": "ERRO", "msg": str(e)}), 400

@app.route('/radar', methods=['GET'])
def monitor_global():
    # Rota secreta para você ver a frota de qualquer navegador
    return jsonify({"info": "SISTEMA STEALTH ATIVO - ACESSO RESTRITO"}), 403

if __name__ == "__main__":
    # Roda na porta 5000 para o Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

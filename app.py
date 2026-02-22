from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>FLYING FORTRESS SECURITY</h1><p>Status: SISTEMA OPERACIONAL - AGUARDANDO COMANDO</p>"

@app.route('/registrar', methods=['POST'])
def registrar_global():
    try:
        dados = request.json
        return jsonify({"status": "SUCESSO", "msg": "Piloto Autenticado"}), 200
    except Exception as e:
        return jsonify({"status": "ERRO", "msg": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

from flask import Flask, jsonify, request
from flask_cors import CORS


# Crear la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde cualquier origen
CORS(app)


# Ruta principal que devuelve la IP del cliente y una suma sencilla
@app.route('/api/hello', methods=['GET'])
def hello_world():
    # Obtener la IP del cliente
    client_ip = request.remote_addr
    # Realizar una suma sencilla
    suma = 5 + 3
    return jsonify({
        "message": "Hello, if you see this, EC2 WORKS!",
        "client_ip": client_ip,
        "suma": f"5 + 3 = {suma}",
        "resultado": suma
    })


# Ruta de inicio como alternativa
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API is available. Use /api/hello for the message"})


# Ejecutar la app si este script es ejecutado directamente
if __name__ == '__main__':
    # Modo de depuración activado y permitiendo conexiones desde cualquier IP
    # Obtener puerto desde variable de entorno para Heroku o usar 5000 por defecto
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

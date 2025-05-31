from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime

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


@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API de Gestión de Inventario disponible. Consulta /api/docs para más información."})

import requests

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    
    # Verificar si se tiene instalado requests
    try:
        import requests
    except ImportError:
        print("No se encuentra el módulo 'requests' instalado. Instalalo con 'pip install requests' y vuelve a intentarlo.")
        exit(1)
    
    url = "http://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    products = response.json()
    
    if category:
        filtered_products = [product for product in products if product['category'] == category]
        return jsonify({
            "status": "success",
            "message": f"Productos en la categoría {category}",
            "count": len(filtered_products),
            "data": filtered_products
        })
    
    return jsonify({
        "status": "success",
        "message": "Lista de todos los productos",
        "count": len(products),
        "data": products
    })

    data = request.get_json()
    
    if not data or 'customer_id' not in data or 'products' not in data:
        return jsonify({
            "status": "error",
            "message": "Datos incompletos. Se requiere customer_id y products."
        }), 400
    
    # Verificar que el cliente existe
    if data['customer_id'] not in customers_db:
        return jsonify({
            "status": "error",
            "message": f"Cliente con ID {data['customer_id']} no encontrado."
        }), 404
    
    # Verificar stock de productos
    total = 0
    order_items = []
    
    for product_item in data['products']:
        product_id = product_item.get('id')
        quantity = product_item.get('quantity', 1)
        
        if product_id not in products_db:
            return jsonify({
                "status": "error",
                "message": f"Producto con ID {product_id} no encontrado."
            }), 404
        
        product = products_db[product_id]
        
        if product['stock'] < quantity:
            return jsonify({
                "status": "error",
                "message": f"Stock insuficiente para {product['name']}. Disponible: {product['stock']}"
            }), 400
        
        # Calcular subtotal
        subtotal = product['price'] * quantity
        total += subtotal
        
        # Actualizar stock
        products_db[product_id]['stock'] -= quantity
        
        # Agregar a los items de la orden
        order_items.append({
            "product_id": product_id,
            "name": product['name'],
            "price": product['price'],
            "quantity": quantity,
            "subtotal": subtotal
        })
    
    # Crear la orden
    order_id = str(uuid.uuid4())
    order = {
        "id": order_id,
        "customer_id": data['customer_id'],
        "customer_name": customers_db[data['customer_id']]['name'],
        "items": order_items,
        "total": total,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    orders_db[order_id] = order
    
    return jsonify({
        "status": "success",
        "message": "Orden creada exitosamente",
        "data": order
    }), 201

# API 3: Obtener categorías de productos
@app.route('/api/categories', methods=['GET'])
def get_categories():
    url = "https://api.escuelajs.co/api/v1/categories"
    response = requests.get(url)
    categories = response.json()
    return jsonify({
        "status": "success",
        "message": "Lista de categorías",
        "count": len(categories),
        "data": categories
    })


# API 4: Obtener detalles de un cliente y sus órdenes
@app.route('/api/users', methods=['GET'])
def get_customer():
    url = "https://api.escuelajs.co/api/v1/users"
    response = requests.get(url)
    users = response.json()
    return jsonify({
        "status": "success",
        "message": "Lista de usuarios",
        "count": len(users),
        "data": users
    })
    
    # Obtener datos del cliente
    customer = customers_db[customer_id]
    
    # Buscar órdenes del cliente
    customer_orders = [order for order in orders_db.values() if order['customer_id'] == customer_id]
    
    return jsonify({
        "status": "success",
        "message": f"Detalles del cliente {customer['name']}",
        "data": {
            "customer": customer,
            "orders": customer_orders,
            "order_count": len(customer_orders)
        }
    })

# Documentación de la API
@app.route('/api/docs', methods=['GET'])
def api_docs():
    return jsonify({
        "api_name": "Sistema de Gestión de Inventario",
        "version": "1.0",
        "endpoints": [
            {
                "path": "/api/products",
                "method": "GET",
                "description": "Obtener todos los productos o filtrar por categoría",
                "params": ["category (opcional): Filtrar por categoría"]
            },
            {
                "path": "/api/orders",
                "method": "POST",
                "description": "Crear una nueva orden",
                "body": {
                    "customer_id": "ID del cliente",
                    "products": [{
                        "id": "ID del producto",
                        "quantity": "Cantidad (opcional, por defecto 1)"
                    }]
                }
            },
            {
                "path": "/api/categories",
                "method": "GET",
                "description": "Obtener todas las categorías de productos"
            },
            {
                "path": "/api/customers/<customer_id>",
                "method": "GET",
                "description": "Obtener detalles de un cliente y sus órdenes"
            }
        ]
    })

# Ejecutar la app si este script es ejecutado directamente
if __name__ == '__main__':
    # Modo de depuración activado y permitiendo conexiones desde cualquier IP
    # Obtener puerto desde variable de entorno o usar 5000 por defecto
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

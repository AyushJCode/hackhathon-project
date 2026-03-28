from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('products', __name__)

# POST /api/products/add
@bp.route('/api/products/add', methods=['POST'])
def add_product():
    body = request.get_json()

    if not body or 'name' not in body:
        return jsonify({"error": "Name is required"}), 400

    name          = body['name'].strip()
    category      = body.get('category', '').strip()
    current_stock = body.get('current_stock', 0)
    reorder_point = body.get('reorder_point')

    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    if current_stock < 0:
        return jsonify({"error": "Stock cannot be negative"}), 400
    if not reorder_point or reorder_point <= 0:
        return jsonify({"error": "Reorder point must be greater than 0"}), 400

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, current_stock, reorder_point) VALUES (?, ?, ?, ?)",
        (name, category, current_stock, reorder_point)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Product added", "id": new_id}), 201


# GET /api/products
@bp.route('/api/products', methods=['GET'])
def get_products():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200


# GET /api/products/<id>
@bp.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(dict(row)), 200


# PUT /api/products/update/<id>
@bp.route('/api/products/update/<int:id>', methods=['PUT'])
def update_product(id):
    body = request.get_json()

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    name          = body.get('name', row['name'])
    category      = body.get('category', row['category'])
    current_stock = body.get('current_stock', row['current_stock'])
    reorder_point = body.get('reorder_point', row['reorder_point'])

    cursor.execute(
        "UPDATE products SET name=?, category=?, current_stock=?, reorder_point=? WHERE id=?",
        (name, category, current_stock, reorder_point, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Product updated"}), 200


# DELETE /api/products/delete/<id>
@bp.route('/api/products/delete/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product deleted"}), 200
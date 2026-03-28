from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('product_vendors', __name__)

# POST /api/product-vendors/add
@bp.route('/api/product-vendors/add', methods=['POST'])
def add_product_vendor():
    body = request.get_json()

    if not body or 'product_id' not in body or 'vendor_id' not in body:
        return jsonify({"error": "product_id and vendor_id are required"}), 400

    product_id    = body['product_id']
    vendor_id     = body['vendor_id']
    price         = body.get('price')
    min_order_qty = body.get('min_order_qty')

    if not price or not min_order_qty:
        return jsonify({"error": "price and min_order_qty are required"}), 400

    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    cursor.execute("SELECT * FROM vendors WHERE id = ?", (vendor_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Vendor not found"}), 404

    cursor.execute(
        "INSERT INTO product_vendors (product_id, vendor_id, price, min_order_qty) VALUES (?, ?, ?, ?)",
        (product_id, vendor_id, price, min_order_qty)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Product linked to vendor", "id": new_id}), 201


# GET /api/product-vendors/<product_id>
@bp.route('/api/product-vendors/<int:product_id>', methods=['GET'])
def get_product_vendors(product_id):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    cursor.execute('''
        SELECT pv.id, v.name as vendor_name, v.email,
               v.reliability_score, v.lead_time_days,
               pv.price, pv.min_order_qty
        FROM product_vendors pv
        JOIN vendors v ON pv.vendor_id = v.id
        WHERE pv.product_id = ?
    ''', (product_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200
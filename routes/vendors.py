from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('vendors', __name__)

# POST /api/vendors/add
@bp.route('/api/vendors/add', methods=['POST'])
def add_vendor():
    body = request.get_json()

    if not body or 'name' not in body:
        return jsonify({"error": "Name is required"}), 400

    name              = body['name'].strip()
    email             = body.get('email', '').strip()
    reliability_score = body.get('reliability_score', 0)
    lead_time_days    = body.get('lead_time_days', 0)

    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400
    if reliability_score < 0 or reliability_score > 100:
        return jsonify({"error": "Reliability score must be between 0 and 100"}), 400

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vendors (name, email, reliability_score, lead_time_days) VALUES (?, ?, ?, ?)",
        (name, email, reliability_score, lead_time_days)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Vendor added", "id": new_id}), 201


# GET /api/vendors
@bp.route('/api/vendors', methods=['GET'])
def get_vendors():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200


# GET /api/vendors/<id>
@bp.route('/api/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Vendor not found"}), 404

    return jsonify(dict(row)), 200


# PUT /api/vendors/update/<id>
@bp.route('/api/vendors/update/<int:id>', methods=['PUT'])
def update_vendor(id):
    body = request.get_json()

    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors WHERE id = ?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Vendor not found"}), 404

    name              = body.get('name', row['name'])
    email             = body.get('email', row['email'])
    reliability_score = body.get('reliability_score', row['reliability_score'])
    lead_time_days    = body.get('lead_time_days', row['lead_time_days'])

    cursor.execute(
        "UPDATE vendors SET name=?, email=?, reliability_score=?, lead_time_days=? WHERE id=?",
        (name, email, reliability_score, lead_time_days, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Vendor updated"}), 200


# DELETE /api/vendors/delete/<id>
@bp.route('/api/vendors/delete/<int:id>', methods=['DELETE'])
def delete_vendor(id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendors WHERE id = ?", (id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Vendor not found"}), 404

    cursor.execute("DELETE FROM vendors WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Vendor deleted"}), 200
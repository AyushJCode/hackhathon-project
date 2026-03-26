from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('data', __name__)

@bp.route('/add-data', methods=['POST'])
def add_data():
    body = request.get_json()

    if not body or 'user_id' not in body or 'data' not in body:
        return jsonify({"error": "Missing user_id or data"}), 400

    user_id = body['user_id']
    data = body['data'].strip()

    if not data:
        return jsonify({"error": "Data cannot be empty"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (user_id, data) VALUES (?, ?)",
        (user_id, data)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Entry added", "id": new_id}), 201


@bp.route('/get-data', methods=['GET'])
def get_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200


@bp.route('/reset', methods=['DELETE'])
def reset():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries")
    conn.commit()
    conn.close()

    return jsonify({"message": "All entries deleted"}), 200
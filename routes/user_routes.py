from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('users', __name__)

@bp.route('/add-user', methods=['POST'])
def add_user():
    body = request.get_json()

    if not body or 'name' not in body or 'email' not in body:
        return jsonify({"error": "Missing name or email"}), 400

    name = body['name'].strip()
    email = body['email'].strip()

    if not name or not email:
        return jsonify({"error": "Name and email cannot be empty"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": "User created", "id": new_id}), 201

    except Exception as e:
        conn.close()
        return jsonify({"error": "Email already exists"}), 409
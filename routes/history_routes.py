from flask import Blueprint, request, jsonify
from database import get_connection

bp = Blueprint('history', __name__)

@bp.route('/history', methods=['GET'])
def history():
    user_id = request.args.get('user_id')

    conn = get_connection()
    cursor = conn.cursor()

    if user_id:
        cursor.execute(
            "SELECT * FROM entries WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
    else:
        cursor.execute("SELECT * FROM entries ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200
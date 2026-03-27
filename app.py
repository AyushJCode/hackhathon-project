from flask import Flask
from database import init_db
from routes.data_routes import bp as data_bp
from routes.history_routes import bp as history_bp
from routes.user_routes import bp as user_bp

app = Flask(__name__)

with app.app_context():
    init_db()

app.register_blueprint(data_bp)
app.register_blueprint(history_bp)
app.register_blueprint(user_bp)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
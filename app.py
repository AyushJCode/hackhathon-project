from flask import Flask
from database import init_db
from routes.products import bp as products_bp
from routes.vendors import bp as vendors_bp
from routes.product_vendors import bp as product_vendors_bp

app = Flask(__name__)

with app.app_context():
    init_db()

app.register_blueprint(products_bp)
app.register_blueprint(vendors_bp)
app.register_blueprint(product_vendors_bp)

@app.route('/')
def index():
    return "Backend is running."

if __name__ == "__main__":
    app.run(debug=True)
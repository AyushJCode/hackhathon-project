from flask import Flask
from database import init_db
from routes.data_routes import bp as data_bp
from routes.history_routes import bp as history_bp

app = Flask(__name__)

with app.app_context():
    init_db()

app.register_blueprint(data_bp)
app.register_blueprint(history_bp)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)



'''
---

**Folder structure should look exactly like this:**
'''
# hackathon-project/
# ├── app.py
# ├── database.py
# ├── hackathon.db        ← auto-created when you run app.py
# └── routes/
#     ├── __init__.py
#     ├── data_routes.py
#     └── history_routes.py
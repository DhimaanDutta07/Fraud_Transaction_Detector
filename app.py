from flask import Flask, render_template
from config import Config
from db.mongo import init_mongo
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

# Initialize MongoDB
init_mongo(app)

# Register blueprints
from auth.routes import auth_bp
from fraud.routes import fraud_bp

app.register_blueprint(auth_bp)
app.register_blueprint(fraud_bp)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error', 'details': str(error)}, 500

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Route not found'}, 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)

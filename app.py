from flask import Flask, render_template
from config import Config
from db.mongo import init_mongo

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

init_mongo(app)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

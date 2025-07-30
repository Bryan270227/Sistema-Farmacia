# app/app.py
from flask import Flask
from flask_cors import CORS
from .db import db, init_db  # Usa una ruta relativa para importar db
from .auth.auth import auth_bp
from .routes.ofertas import ofertas_bp
from app.routes.capacitaciones import capacitaciones_bp
from .routes.inscripciones import inscripciones_bp
from .routes.reportes import reportes_bp

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:17062001@localhost/farmacia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la aplicación
init_db(app)

# Registrar blueprints (rutas)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(ofertas_bp, url_prefix="/api/ofertas")
app.register_blueprint(capacitaciones_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(reportes_bp)

# Ruta raíz para verificar que la API está funcionando
@app.route("/")
def index():
    return "API de Farmacia Santa Martha funcionando", 200
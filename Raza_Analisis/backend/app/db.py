# app/db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Inicializa la base de datos y crea las tablas si no existen.
    """
    db.init_app(app)
    with app.app_context():
        from .models import User, JobOffer, Course, Enrollment  # Importa los modelos
        db.create_all()
        print("✅ Tablas creadas correctamente")
from flask import Blueprint, request, jsonify
from app.models import Enrollment, User, Course
from app.db import db
from datetime import datetime
from app.schemas import EnrollmentCreate
from functools import wraps
from app.auth.utils import validate_token

# Middleware para verificar autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token no válido o faltante"}), 401
        try:
            user_id = validate_token(token.split(" ")[1])
        except Exception:
            return jsonify({"error": "Token inválido"}), 401

        current_user = User.query.get(user_id)
        if not current_user:
            return jsonify({"error": "Usuario no encontrado"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

inscripciones_bp = Blueprint('inscripciones', __name__, url_prefix="/api/inscripciones")

# Registrar una nueva inscripción
@inscripciones_bp.route('', methods=['POST'])
def registrar_inscripcion():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token faltante"}), 401

        token = auth_header.split(" ")[1]
        user_id = validate_token(token)

        data = request.get_json()
        course_id = data.get("curso_id")
        if not course_id:
            return jsonify({"error": "ID del curso faltante"}), 400

        curso = Course.query.get(course_id)
        if not curso:
            return jsonify({"error": "El curso no existe"}), 404

        existente = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existente:
            return jsonify({"error": "Ya estás inscrito en este curso"}), 409

        inscripcion = Enrollment(user_id=user_id, course_id=course_id, fecha_inscripcion=datetime.utcnow())
        db.session.add(inscripcion)
        db.session.commit()

        return jsonify({"message": "Inscripción registrada exitosamente"}), 201

    except Exception as e:
        print(f"❌ Error en inscripción: {e}")
        return jsonify({"error": str(e)}), 500

# Listar todas las inscripciones (con email del usuario)
@inscripciones_bp.route('/', methods=['GET'])
def listar_inscripciones():
    try:
        inscripciones = Enrollment.query.all()
        return jsonify([
            {
                "usuario": i.user.username,
                "email": i.user.email,
                "curso": i.course.titulo,
                "fecha_inscripcion": i.fecha_inscripcion.strftime('%Y-%m-%d')
            }
            for i in inscripciones
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar inscripciones por usuario autenticado
@inscripciones_bp.route('/usuario', methods=['GET'])
@token_required
def obtener_inscripciones_usuario(current_user):
    try:
        inscripciones = Enrollment.query.filter_by(user_id=current_user.id).all()
        resultado = []
        for inscripcion in inscripciones:
            resultado.append({
                "id": inscripcion.id,
                "curso_id": inscripcion.course.id,
                "titulo": inscripcion.course.titulo,
                "descripcion": inscripcion.course.descripcion,
                "fecha_inicio": inscripcion.course.fecha_inicio.strftime('%Y-%m-%d'),
                "fecha_fin": inscripcion.course.fecha_fin.strftime('%Y-%m-%d'),
                "fecha_inscripcion": inscripcion.fecha_inscripcion.strftime('%Y-%m-%d %H:%M')
            })
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

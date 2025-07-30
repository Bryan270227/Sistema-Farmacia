from flask import Blueprint, request, jsonify
from ..crud import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course,
)
from datetime import datetime
from app.auth.utils import validate_token

# Definición del Blueprint
capacitaciones_bp = Blueprint('capacitaciones', __name__, url_prefix="/api/cursos")

# Ruta para preflight OPTIONS (CORS)
@capacitaciones_bp.route('', methods=['OPTIONS'])
def preflight():
    response = jsonify({"message": "Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    return response, 200

# Crear una nueva capacitación
@capacitaciones_bp.route('', methods=['POST'])
def crear_capacitacion():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()

        # Validar campos obligatorios
        required_fields = [
            'titulo',
            'descripcion',
            'duracion_horas',
            'fecha_inicio',
            'fecha_fin',
            'instructor',
            'cupo_maximo',
        ]
        if not all(field in data and data[field] is not None for field in required_fields):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Extraer datos
        titulo = data['titulo']
        descripcion = data['descripcion']
        duracion_horas = data['duracion_horas']
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        instructor = data['instructor']
        cupo_maximo = data['cupo_maximo']
        estado = data.get('estado', 'activo')  # Estado por defecto: activo

        # Crear el curso en la base de datos
        curso = create_course(
            titulo=titulo,
            descripcion=descripcion,
            duracion_horas=duracion_horas,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            instructor=instructor,
            cupo_maximo=cupo_maximo,
            estado=estado,
        )

        # Respuesta exitosa
        return jsonify({
            "message": "Capacitación creada exitosamente",
            "curso": {
                "id": curso.id,
                "titulo": curso.titulo,
                "descripcion": curso.descripcion,
                "duracion_horas": curso.duracion_horas,
                "fecha_inicio": curso.fecha_inicio.strftime('%Y-%m-%d'),
                "fecha_fin": curso.fecha_fin.strftime('%Y-%m-%d'),
                "instructor": curso.instructor,
                "cupo_maximo": curso.cupo_maximo,
                "estado": curso.estado,
            },
        }), 201

    except Exception as e:
        # Manejo de errores
        return jsonify({"error": f"Error al crear la capacitación: {str(e)}"}), 500

# Obtener todas las capacitaciones
@capacitaciones_bp.route('', methods=['GET'])
def obtener_capacitaciones():
    try:
        print(">> Obteniendo capacitaciones...")
        cursos = get_all_courses()
        print(f">> Se encontraron {len(cursos)} cursos")

        cursos_formateados = [
            {
                "id": curso.id,
                "titulo": curso.titulo,
                "descripcion": curso.descripcion,
                "duracion_horas": curso.duracion_horas,
                "fecha_inicio": curso.fecha_inicio.strftime('%Y-%m-%d'),
                "fecha_fin": curso.fecha_fin.strftime('%Y-%m-%d'),
                "instructor": curso.instructor,
                "cupo_maximo": curso.cupo_maximo,
                "estado": curso.estado.value,
            }
            for curso in cursos
        ]
        return jsonify({"cursos": cursos_formateados}), 200

    except Exception as e:
        print(f">> ERROR al obtener capacitaciones: {e}")
        return jsonify({"error": f"Error al obtener las capacitaciones: {str(e)}"}), 500

# Obtener una capacitación por ID
@capacitaciones_bp.route('/<int:id>', methods=['GET'])
def obtener_capacitacion_por_id(id):
    try:
        print(f">> Buscando capacitación con ID: {id}")
        curso = get_course_by_id(id)

        if not curso:
            print(">> No se encontró el curso con ese ID")
            return jsonify({"error": "Capacitación no encontrada"}), 404

        curso_formateado = {
            "id": curso.id,
            "titulo": curso.titulo,
            "descripcion": curso.descripcion,
            "duracion_horas": curso.duracion_horas,
            "fecha_inicio": curso.fecha_inicio.strftime('%Y-%m-%d'),
            "fecha_fin": curso.fecha_fin.strftime('%Y-%m-%d'),
            "instructor": curso.instructor,
            "cupo_maximo": curso.cupo_maximo,
            "estado": curso.estado.value,
        }

        return jsonify(curso_formateado), 200

    except Exception as e:
        return jsonify({"error": f"Error al obtener la capacitación: {str(e)}"}), 500

# Editar una capacitación existente
@capacitaciones_bp.route('/<int:id>', methods=['PUT'])
def editar_capacitacion(id):
    try:
        curso = get_course_by_id(id)
        if not curso:
            return jsonify({"error": "Capacitación no encontrada"}), 404

        data = request.get_json()

        curso.titulo = data.get('titulo', curso.titulo)
        curso.descripcion = data.get('descripcion', curso.descripcion)
        curso.duracion_horas = data.get('duracion_horas', curso.duracion_horas)
        curso.fecha_inicio = datetime.strptime(data.get('fecha_inicio', curso.fecha_inicio.strftime('%Y-%m-%d')), "%Y-%m-%d").date()
        curso.fecha_fin = datetime.strptime(data.get('fecha_fin', curso.fecha_fin.strftime('%Y-%m-%d')), "%Y-%m-%d").date()
        curso.instructor = data.get('instructor', curso.instructor)
        curso.cupo_maximo = data.get('cupo_maximo', curso.cupo_maximo)
        curso.estado = data.get('estado', curso.estado)

        updated = update_course(curso)

        return jsonify({
            "message": "Capacitación actualizada exitosamente",
            "curso": {
                "id": updated.id,
                "titulo": updated.titulo,
                "descripcion": updated.descripcion,
                "duracion_horas": updated.duracion_horas,
                "fecha_inicio": updated.fecha_inicio.strftime('%Y-%m-%d'),
                "fecha_fin": updated.fecha_fin.strftime('%Y-%m-%d'),
                "instructor": updated.instructor,
                "cupo_maximo": updated.cupo_maximo,
                "estado": updated.estado.value,  # <-- ¡CORREGIDO!
            },
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error al actualizar la capacitación: {str(e)}"}), 500

# Eliminar una capacitación
@capacitaciones_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_capacitacion(id):
    try:
        curso = get_course_by_id(id)
        if not curso:
            return jsonify({"error": "Capacitación no encontrada"}), 404

        delete_course(curso)
        return jsonify({"message": "Capacitación eliminada exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar la capacitación: {str(e)}"}), 500
 
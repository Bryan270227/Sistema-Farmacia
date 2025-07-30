from flask import Blueprint, request, jsonify
from app.models import JobOffer, Application, User
from app.db import db
from app.auth.utils import validate_token
from ..crud import (
    create_job_offer,
    get_all_offers,
    get_offer_by_id,
    update_offer,
    delete_offer
)


ofertas_bp = Blueprint("ofertas", __name__, url_prefix="/api/ofertas")

# Crear una nueva oferta laboral
@ofertas_bp.route('', methods=['POST'])
def crear_oferta():
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        requisitos = data.get('requisitos')

        if not titulo or not descripcion:
            return jsonify({"error": "Título y descripción son obligatorios"}), 400

        oferta = create_job_offer(titulo, descripcion, requisitos)

        return jsonify({
            "message": "Oferta creada exitosamente",
            "oferta": {
                "id": oferta.id,
                "titulo": oferta.titulo,
                "descripcion": oferta.descripcion,
                "requisitos": oferta.requisitos,
                "fecha_publicacion": oferta.fecha_publicacion.strftime('%Y-%m-%d')
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener todas las ofertas laborales
@ofertas_bp.route("", methods=["GET"])
def obtener_ofertas():
    try:
        ofertas = get_all_offers()
        lista = [
            {
                "id": o.id,
                "titulo": o.titulo,
                "descripcion": o.descripcion,
                "requisitos": o.requisitos,
                "fecha_publicacion": o.fecha_publicacion.strftime('%Y-%m-%d')
            }
            for o in ofertas
        ]
        return jsonify({"ofertas": lista}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Obtener una oferta específica por ID
@ofertas_bp.route("/<int:oferta_id>", methods=["GET"])
def obtener_oferta(oferta_id):
    try:
        oferta = get_offer_by_id(oferta_id)
        if not oferta:
            return jsonify({"error": "Oferta no encontrada"}), 404

        return jsonify({
            "id": oferta.id,
            "titulo": oferta.titulo,
            "descripcion": oferta.descripcion,
            "requisitos": oferta.requisitos,
            "fecha_publicacion": oferta.fecha_publicacion.strftime('%Y-%m-%d')
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Actualizar una oferta laboral
@ofertas_bp.route("/<int:oferta_id>", methods=["PUT"])
def actualizar_oferta(oferta_id):
    try:
        data = request.get_json()
        oferta_actualizada = update_offer(oferta_id, data)
        if not oferta_actualizada:
            return jsonify({"error": "Oferta no encontrada"}), 404

        return jsonify({
            "message": "Oferta actualizada correctamente",
            "oferta": {
                "id": oferta_actualizada.id,
                "titulo": oferta_actualizada.titulo,
                "descripcion": oferta_actualizada.descripcion,
                "requisitos": oferta_actualizada.requisitos,
                "fecha_publicacion": oferta_actualizada.fecha_publicacion.strftime('%Y-%m-%d')
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Eliminar una oferta laboral
@ofertas_bp.route("/<int:oferta_id>", methods=["DELETE"])
def eliminar_oferta(oferta_id):
    try:
        eliminado = delete_offer(oferta_id)
        if not eliminado:
            return jsonify({"error": "Oferta no encontrada"}), 404

        return jsonify({"message": "Oferta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Postular a una oferta laboral
@ofertas_bp.route('/postular', methods=['POST'])
def postular_oferta():
    try:
        token_header = request.headers.get("Authorization")
        if not token_header or not token_header.startswith("Bearer "):
            return jsonify({"error": "Token faltante"}), 401

        token = token_header.split(" ")[1]
        user_id = validate_token(token)

        data = request.get_json()
        oferta_id = data.get("idOferta")

        if not oferta_id:
            return jsonify({"error": "ID de oferta requerido"}), 400

        # Verifica si ya está postulando
        existe = Application.query.filter_by(user_id=user_id, job_offer_id=oferta_id).first()
        if existe:
            return jsonify({"error": "Ya estás postulado a esta oferta."}), 409

        nueva = Application(user_id=user_id, job_offer_id=oferta_id)
        db.session.add(nueva)
        db.session.commit()

        return jsonify({"message": "✅ Postulación registrada correctamente."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token faltante"}), 401

        token = auth_header.split(" ")[1]
        user_id = validate_token(token)

        data = request.get_json()
        oferta_id = data.get("idOferta")
        if not oferta_id:
            return jsonify({"error": "ID de la oferta faltante"}), 400

        # Verificar si ya está postulado
        ya_postulado = Application.query.filter_by(user_id=user_id, job_offer_id=oferta_id).first()
        if ya_postulado:
            return jsonify({"error": "Ya te has postulado a esta oferta"}), 400

        nueva_postulacion = Application(user_id=user_id, job_offer_id=oferta_id)
        db.session.add(nueva_postulacion)
        db.session.commit()

        return jsonify({"message": "Postulación realizada exitosamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Listar todos los postulantes (vista admin)
@ofertas_bp.route('/postulantes', methods=['GET'])
def listar_postulantes():
    try:
        postulaciones = Application.query.all()
        lista = []
        for p in postulaciones:
            lista.append({
                "nombre_usuario": p.user.username,
                "correo": p.user.email,
                "oferta": p.job_offer.titulo,
                "fecha": p.fecha_postulacion.strftime('%Y-%m-%d')
            })
        return jsonify(lista), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ofertas_bp.route('/mis-postulaciones', methods=['GET'])
def mis_postulaciones():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token faltante"}), 401

        token = auth_header.split(" ")[1]
        user_id = validate_token(token)

        # Filtrar las postulaciones por usuario
        postulaciones = Application.query.filter_by(user_id=user_id).all()

        data = []
        for p in postulaciones:
            data.append({
                "id_postulacion": p.id,
                "titulo": p.job_offer.titulo,
                "descripcion": p.job_offer.descripcion,
                "fecha_postulacion": p.fecha_postulacion.strftime('%Y-%m-%d')
            })

        return jsonify({"postulaciones": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ofertas_bp.route('/postulaciones/<int:postulacion_id>', methods=['DELETE'])
def cancelar_postulacion(postulacion_id):
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token faltante"}), 401

        token = auth_header.split(" ")[1]
        user_id = validate_token(token)

        postulacion = Application.query.filter_by(id=postulacion_id, user_id=user_id).first()
        if not postulacion:
            return jsonify({"error": "Postulación no encontrada"}), 404

        db.session.delete(postulacion)
        db.session.commit()

        return jsonify({"message": "Postulación cancelada correctamente."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

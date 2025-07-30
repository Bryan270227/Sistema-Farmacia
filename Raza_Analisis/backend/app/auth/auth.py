from flask import Blueprint, request, jsonify
from ..models import User
from ..db import db
from .utils import create_token, validate_token
from ..crud import get_user_by_username, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def register():
    data = request.get_json()

    if get_user_by_username(data['username']):
        return jsonify({"error": "El usuario ya existe"}), 400

    if data.get('password') != data.get('confirm_password'):
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    nuevo_usuario = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'usuario')
    )

    create_user(nuevo_usuario)
    return jsonify({"message": "Usuario registrado correctamente"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = get_user_by_username(data['username'])

    if not usuario or usuario.password != data['password']:
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_token(usuario)
    return jsonify({
        "access_token": token,
        "user_id": usuario.id,
        "username": usuario.username,
        "role": usuario.role
    }), 200

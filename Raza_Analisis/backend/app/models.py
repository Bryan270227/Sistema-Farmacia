# app/models.py
from app.db import db  # Usa una ruta relativa para importar db
from datetime import datetime
from enum import Enum


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='usuario')  # 'admin' o 'usuario'

    # Relaciones
    inscripciones = db.relationship('Enrollment', back_populates='user', cascade="all, delete-orphan")
    postulaciones = db.relationship('Application', back_populates='user', cascade="all, delete-orphan")



class JobOffer(db.Model):
    __tablename__ = 'job_offer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    requisitos = db.Column(db.Text)
    fecha_publicacion = db.Column(db.Date, default=datetime.utcnow, nullable=False)

    # Relaciones
    postulaciones = db.relationship('Application', back_populates='job_offer', cascade="all, delete-orphan")


class EstadoCapacitacion(Enum):
    activo = "activo"
    inactivo = "inactivo"

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_horas = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    instructor = db.Column(db.String(255), nullable=False)
    cupo_maximo = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Enum(EstadoCapacitacion), default=EstadoCapacitacion.activo, nullable=False)

    inscripciones = db.relationship('Enrollment', back_populates='course', cascade="all, delete-orphan")

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship('User', back_populates='inscripciones')
    course = db.relationship('Course', back_populates='inscripciones')

class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_offer_id = db.Column(db.Integer, db.ForeignKey('job_offer.id'), nullable=False)
    fecha_postulacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship('User', back_populates='postulaciones')
    job_offer = db.relationship('JobOffer', back_populates='postulaciones')
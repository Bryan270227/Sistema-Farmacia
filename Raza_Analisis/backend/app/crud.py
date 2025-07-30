from app.db import db
from app.models import User, JobOffer, Course, Enrollment
from datetime import datetime

# ------------------------- USUARIOS -------------------------
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def create_user(user):
    db.session.add(user)
    db.session.commit()
    return user

# ------------------------- OFERTAS LABORALES -------------------------
def create_job_offer(titulo, descripcion, requisitos):
    offer = JobOffer(
        titulo=titulo,
        descripcion=descripcion,
        requisitos=requisitos
    )
    db.session.add(offer)
    db.session.commit()
    return offer

def get_all_offers():
    return JobOffer.query.all()

def get_offer_by_id(offer_id):
    return JobOffer.query.get(offer_id)

def update_offer(offer_id, data):
    offer = JobOffer.query.get(offer_id)
    if not offer:
        return None

    offer.titulo = data.get("titulo", offer.titulo)
    offer.descripcion = data.get("descripcion", offer.descripcion)
    offer.requisitos = data.get("requisitos", offer.requisitos)
    offer.fecha_publicacion = datetime.strptime(
        data.get("fecha_publicacion", offer.fecha_publicacion.strftime('%Y-%m-%d')),
        '%Y-%m-%d'
    ).date()

    db.session.commit()
    return offer

def delete_offer(offer_id):
    offer = JobOffer.query.get(offer_id)
    if offer:
        db.session.delete(offer)
        db.session.commit()
        return True
    return False

# ------------------------- CURSOS / CAPACITACIONES -------------------------
def create_course(titulo, descripcion, duracion_horas, fecha_inicio, fecha_fin, instructor, cupo_maximo, estado="activo"):
    course = Course(
        titulo=titulo,
        descripcion=descripcion,
        duracion_horas=duracion_horas,
        fecha_inicio=datetime.strptime(fecha_inicio, "%Y-%m-%d").date(),
        fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d").date(),
        instructor=instructor,
        cupo_maximo=cupo_maximo,
        estado=estado
    )
    db.session.add(course)
    db.session.commit()
    return course

def get_all_courses():
    return Course.query.all()

def get_course_by_id(course_id):
    return Course.query.get(course_id)

def update_course(course):
    db.session.commit()
    return course

def delete_course(course):
    db.session.delete(course)
    db.session.commit()

# ------------------------- INSCRIPCIONES -------------------------
def create_enrollment(user_id, course_id):
    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return enrollment

def get_all_enrollments():
    return Enrollment.query.all()

def get_enrollment_by_id(enrollment_id):
    return Enrollment.query.get(enrollment_id)

def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
        return True
    return False

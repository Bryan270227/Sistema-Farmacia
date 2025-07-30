from flask import Blueprint, Response, request
from app.models import Enrollment, Application
from app.db import db
import csv
import io
from app.auth.utils import validate_token

reportes_bp = Blueprint("reportes", __name__, url_prefix="/api/reportes")

def generar_csv(datos, campos):
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=campos)
    writer.writeheader()
    for row in datos:
        writer.writerow(row)
    buffer.seek(0)
    return buffer.getvalue()

# Reporte de inscripciones
@reportes_bp.route("/inscripciones", methods=["GET"])
def reporte_inscripciones():
    inscripciones = Enrollment.query.all()
    datos = [{
        "Usuario": i.user.username,
        "Correo": i.user.email,
        "Curso": i.course.titulo,
        "Fecha de Inscripción": i.fecha_inscripcion.strftime("%Y-%m-%d")
    } for i in inscripciones]

    contenido = generar_csv(datos, ["Usuario", "Correo", "Curso", "Fecha de Inscripción"])
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=reporte_inscripciones.csv"}
    )

# Reporte de postulaciones
@reportes_bp.route("/postulaciones", methods=["GET"])
def reporte_postulaciones():
    postulaciones = Application.query.all()
    datos = [{
        "Usuario": p.user.username,
        "Correo": p.user.email,
        "Oferta": p.job_offer.titulo,
        "Fecha de Postulación": p.fecha_postulacion.strftime("%Y-%m-%d")
    } for p in postulaciones]

    contenido = generar_csv(datos, ["Usuario", "Correo", "Oferta", "Fecha de Postulación"])
    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=reporte_postulaciones.csv"}
    )

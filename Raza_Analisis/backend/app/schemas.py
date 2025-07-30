from pydantic import BaseModel, EmailStr
from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    admin = "admin"
    usuario = "usuario"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True

class CourseCreate(BaseModel):
    titulo: str
    descripcion: str
    duracion_horas: int
    fecha_inicio: str
    fecha_fin: str
    instructor: str
    cupo_maximo: int
    estado: str

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class EnrollmentOut(BaseModel):
    id: int
    usuario: str
    curso: str
    fecha_inscripcion: str

    class Config:
        orm_mode = True
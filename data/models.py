from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from utils.db import Base

# ---------------------- SQLAlchemy Models ----------------------

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    equipo = Column(String, nullable=False)
    posicion = Column(String, nullable=False)
    edad = Column(Integer, nullable=False)
    nacionalidad = Column(String, nullable=False)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    eliminado = Column(Boolean, default=False)
    eliminado_logico = Column(Boolean, default=False)

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais = Column(String, nullable=False)
    grupo = Column(String, nullable=False)
    eliminado = Column(Boolean, default=False)
    eliminado_logico = Column(Boolean, default=False)

# ---------------------- Pydantic Schemas ----------------------

# Jugador

class JugadorBase(BaseModel):
    nombre: str
    equipo: str
    posicion: str
    edad: int
    nacionalidad: str
    goles: int
    asistencias: int
    eliminado: bool = False

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(JugadorBase):
    pass

class JugadorWithId(JugadorBase):
    id: int
    eliminado_logico: bool

    class Config:
        from_attributes = True

# Equipo

class EquipoBase(BaseModel):
    nombre: str
    pais: str
    grupo: str
    eliminado: bool = False

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(EquipoBase):
    pass

class EquipoWithId(EquipoBase):
    id: int
    eliminado_logico: bool

    class Config:
        from_attributes = True

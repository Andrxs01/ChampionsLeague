# models.py
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
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
    nombre: str = Field(..., example="Cristiano Ronaldo")
    equipo: str = Field(..., example="Real Madrid")
    posicion: str = Field(..., example="Delantero")
    edad: int = Field(..., ge=15, le=50, example=32)
    nacionalidad: str = Field(..., example="Portugal")
    goles: int = Field(default=0, ge=0)
    asistencias: int = Field(default=0, ge=0)
    eliminado: bool = Field(default=False, example=False)

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(JugadorBase):
    pass

class JugadorWithId(JugadorBase):
    id: int

    class Config:
        from_attributes = True

# Equipo

class EquipoBase(BaseModel):
    nombre: str = Field(..., example="Real Madrid")
    pais: str = Field(..., example="España")
    grupo: str = Field(..., example="H")
    eliminado: bool = Field(default=False, example=False)

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(EquipoBase):
    pass

class EquipoWithId(EquipoBase):
    id: int

    class Config:
        from_attributes = True
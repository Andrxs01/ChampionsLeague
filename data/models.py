# data/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import date

Base = declarative_base()

# Esquemas Pydantic para validación de datos
class JugadorBase(BaseModel):
    nombre: str
    equipo_id: int
    posicion: str
    edad: int
    nacionalidad: str
    goles: int = 0
    asistencias: int = 0

class JugadorCreate(JugadorBase):
    pass

class JugadorUpdate(JugadorBase):
    eliminado_logico: bool = False
    nombre: Optional[str] = None
    equipo_id: Optional[int] = None
    posicion: Optional[str] = None
    edad: Optional[int] = None
    nacionalidad: Optional[str] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    posicion = Column(String)
    edad = Column(Integer)
    nacionalidad = Column(String)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    eliminado_logico = Column(Boolean, default=False)

    equipo_obj = relationship("Equipo", back_populates="jugadores")

    # Configuración para Pydantic (para serialización)
    class Config:
        from_attributes = True

class EquipoBase(BaseModel):
    nombre: str
    pais: str
    grupo: str
    imagen_url: Optional[HttpUrl] = None # Mantenemos la URL para la imagen del equipo

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(EquipoBase):
    eliminado_logico: bool = False
    nombre: Optional[str] = None
    pais: Optional[str] = None
    grupo: Optional[str] = None
    imagen_url: Optional[HttpUrl] = None

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    pais = Column(String)
    grupo = Column(String)
    imagen_url = Column(String, nullable=True) # Almacenamos la URL como String
    eliminado_logico = Column(Boolean, default=False)

    jugadores = relationship("Jugador", back_populates="equipo_obj")
    partidos_local = relationship("Partido", foreign_keys="[Partido.equipo_local_id]", back_populates="equipo_local_obj")
    partidos_visitante = relationship("Partido", foreign_keys="[Partido.equipo_visitante_id]", back_populates="equipo_visitante_obj")

    class Config:
        from_attributes = True

# --- NUEVO MODELO PARA PARTIDOS ---
class PartidoBase(BaseModel):
    equipo_local_id: int
    equipo_visitante_id: int
    goles_local: int
    goles_visitante: int
    fecha: date
    fase: str # Ej: "Fase de Grupos", "Octavos de Final", "Cuartos de Final", "Semifinal", "Final"

class PartidoCreate(PartidoBase):
    pass

class PartidoUpdate(PartidoBase):
    equipo_local_id: Optional[int] = None
    equipo_visitante_id: Optional[int] = None
    goles_local: Optional[int] = None
    goles_visitante: Optional[int] = None
    fecha: Optional[date] = None
    fase: Optional[str] = None
    eliminado_logico: bool = False

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_local_id = Column(Integer, ForeignKey("equipos.id"))
    equipo_visitante_id = Column(Integer, ForeignKey("equipos.id"))
    goles_local = Column(Integer)
    goles_visitante = Column(Integer)
    fecha = Column(Date)
    fase = Column(String)
    eliminado_logico = Column(Boolean, default=False)

    equipo_local_obj = relationship("Equipo", foreign_keys=[equipo_local_id], back_populates="partidos_local")
    equipo_visitante_obj = relationship("Equipo", foreign_keys=[equipo_visitante_id], back_populates="partidos_visitante")

    class Config:
        from_attributes = True

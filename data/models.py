# data/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from utils.db import Base # Importa Base desde utils.db
from pydantic import BaseModel, HttpUrl # Importa BaseModel y HttpUrl de Pydantic
from typing import Optional, List # Importa Optional y List para tipos de Pydantic

# --- Modelos de SQLAlchemy (para la base de datos) ---

class Equipo(Base):
    __tablename__ = "equipos" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Clave primaria, indexada para búsquedas rápidas
    nombre = Column(String, unique=True, index=True, nullable=False) # Nombre del equipo, único y no nulo
    pais = Column(String, nullable=False) # País del equipo
    grupo = Column(String, nullable=False) # Grupo de la Champions League (ej. "A", "B")
    imagen_url = Column(String, nullable=True) # URL de la imagen del logo del equipo (puede ser nulo)
    eliminado = Column(Boolean, default=False) # Campo para eliminación física (no usado directamente en soft-delete)
    eliminado_logico = Column(Boolean, default=False) # Campo para eliminación lógica (ocultar en la UI)

    # Relación con la tabla Jugador: un Equipo puede tener muchos Jugadores
    # back_populates="equipo_obj" crea una relación bidireccional
    jugadores = relationship("Jugador", back_populates="equipo_obj")

    def __repr__(self):
        return f"<Equipo(id={self.id}, nombre='{self.nombre}', pais='{self.pais}')>"

class Jugador(Base):
    __tablename__ = "jugadores" # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Clave primaria, indexada
    nombre = Column(String, index=True, nullable=False) # Nombre del jugador
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=False) # Clave foránea que referencia a Equipo
    posicion = Column(String, nullable=False) # Posición del jugador (ej. "Delantero", "Defensa")
    edad = Column(Integer, nullable=False) # Edad del jugador
    nacionalidad = Column(String, nullable=False) # Nacionalidad del jugador
    goles = Column(Integer, default=0) # Número de goles (por defecto 0)
    asistencias = Column(Integer, default=0) # Número de asistencias (por defecto 0)
    imagen_url = Column(String, nullable=True) # URL de la imagen del jugador (puede ser nulo)
    eliminado = Column(Boolean, default=False) # Campo para eliminación física
    eliminado_logico = Column(Boolean, default=False) # Campo para eliminación lógica

    # Relación con la tabla Equipo: un Jugador pertenece a un Equipo
    equipo_obj = relationship("Equipo", back_populates="jugadores")

    def __repr__(self):
        return f"<Jugador(id={self.id}, nombre='{self.nombre}', equipo_id={self.equipo_id})>"

# --- Esquemas de Pydantic (para validación de datos en la API) ---

# Schema base para Equipo (usado para crear)
class EquipoCreate(BaseModel):
    nombre: str
    pais: str
    grupo: str
    imagen_url: Optional[str] = None # HttpUrl si quieres validación estricta de URL, pero str es más flexible para rutas locales

# Schema para actualizar Equipo (todos los campos son opcionales)
class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None
    grupo: Optional[str] = None
    imagen_url: Optional[str] = None
    eliminado_logico: Optional[bool] = None # Permite actualizar el estado de eliminación lógica

# Schema para la respuesta de Equipo (incluye el ID y los campos de DB)
class EquipoWithId(EquipoCreate):
    id: int
    eliminado: bool
    eliminado_logico: bool

    class Config:
        from_attributes = True # Permite que Pydantic lea directamente de los modelos de SQLAlchemy

# Schema base para Jugador (usado para crear)
class JugadorCreate(BaseModel):
    nombre: str
    equipo_id: int # ID del equipo al que pertenece
    posicion: str
    edad: int
    nacionalidad: str
    goles: Optional[int] = 0
    asistencias: Optional[int] = 0
    imagen_url: Optional[str] = None

# Schema para actualizar Jugador (todos los campos son opcionales)
class JugadorUpdate(BaseModel):
    nombre: Optional[str] = None
    equipo_id: Optional[int] = None
    posicion: Optional[str] = None
    edad: Optional[int] = None
    nacionalidad: Optional[str] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None
    imagen_url: Optional[str] = None
    eliminado_logico: Optional[bool] = None # Permite actualizar el estado de eliminación lógica

# Schema para la respuesta de Jugador (incluye el ID y los campos de DB)
class JugadorWithId(JugadorCreate):
    id: int
    eliminado: bool
    eliminado_logico: bool
    # Para incluir el objeto Equipo anidado en la respuesta JSON del jugador
    # equipo_obj: Optional[EquipoWithId] = None # Descomentar si quieres el objeto completo del equipo en la API JSON

    class Config:
        from_attributes = True # Permite que Pydantic lea directamente de los modelos de SQLAlchemy

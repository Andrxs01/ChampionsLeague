# operations/partidos_operations.py
from sqlalchemy.orm import Session, joinedload
from data import models
from data.models import PartidoCreate, PartidoUpdate
from datetime import date
from typing import Optional # <--- ¡Añade esta importación!
from sqlalchemy import or_ # <--- ¡Añade esta importación para usar or_!

# Función para crear un nuevo partido
def create_partido(db: Session, partido: PartidoCreate):
    db_partido = models.Partido(
        equipo_local_id=partido.equipo_local_id,
        equipo_visitante_id=partido.equipo_visitante_id,
        goles_local=partido.goles_local,
        goles_visitante=partido.goles_visitante,
        fecha=partido.fecha,
        fase=partido.fase
    )
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

# Función para obtener todos los partidos
def get_all_partidos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Partido).options(
        joinedload(models.Partido.equipo_local_obj),
        joinedload(models.Partido.equipo_visitante_obj)
    ).filter(
        models.Partido.eliminado_logico == False
    ).order_by(models.Partido.fecha.asc()).offset(skip).limit(limit).all()

# Función para obtener un partido por su ID
def get_partido_by_id(db: Session, partido_id: int):
    return db.query(models.Partido).options(
        joinedload(models.Partido.equipo_local_obj),
        joinedload(models.Partido.equipo_visitante_obj)
    ).filter(
        models.Partido.id == partido_id
    ).first()

# Función para actualizar un partido existente
def update_partido(db: Session, partido_id: int, partido: PartidoUpdate):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido:
        update_data = partido.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_partido, key, value)
        db.commit()
        db.refresh(db_partido)
    return db_partido

# Función para realizar una eliminación lógica de un partido
def soft_delete_partido(db: Session, partido_id: int):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido:
        db_partido.eliminado_logico = True
        db.commit()
        db.refresh(db_partido)
    return db_partido

# Función para buscar partidos por varios criterios (ACTUALIZADA)
def search_partidos(
    db: Session,
    equipo_nombre: Optional[str] = None,
    fase: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    id: Optional[int] = None, # <--- ¡Nuevo parámetro añadido!
    eliminado: bool = False
):
    query = db.query(models.Partido).options(
        joinedload(models.Partido.equipo_local_obj),
        joinedload(models.Partido.equipo_visitante_obj)
    ).filter(models.Partido.eliminado_logico == eliminado)

    if equipo_nombre:
        # Usamos or_ para buscar en el nombre del equipo local O el nombre del equipo visitante
        query = query.filter(
            or_(
                models.Partido.equipo_local_obj.has(models.Equipo.nombre.ilike(f"%{equipo_nombre}%")),
                models.Partido.equipo_visitante_obj.has(models.Equipo.nombre.ilike(f"%{equipo_nombre}%"))
            )
        )
    if fase:
        query = query.filter(models.Partido.fase.ilike(f"%{fase}%"))
    if fecha_inicio:
        query = query.filter(models.Partido.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(models.Partido.fecha <= fecha_fin)
    if id: # <--- ¡Nuevo filtro añadido!
        query = query.filter(models.Partido.id == id)

    return query.all()

# Función para obtener partidos eliminados lógicamente
def get_soft_deleted_partidos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene los partidos que han sido eliminados lógicamente.
    """
    return db.query(models.Partido).options(
        joinedload(models.Partido.equipo_local_obj),
        joinedload(models.Partido.equipo_visitante_obj)
    ).filter(
        models.Partido.eliminado_logico == True
    ).offset(skip).limit(limit).all()
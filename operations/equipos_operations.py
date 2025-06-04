# operations/equipos_operations.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func # Importa func para funciones de agregación
from data import models
from data.models import EquipoCreate, EquipoUpdate

# Función para crear un nuevo equipo en la base de datos
def create_equipo(db: Session, equipo: EquipoCreate):
    db_equipo = models.Equipo(
        nombre=equipo.nombre,
        pais=equipo.pais,
        grupo=equipo.grupo,
        imagen_url=equipo.imagen_url
    )
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

# Función para obtener todos los equipos
def get_all_equipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
        models.Equipo.eliminado_logico == False
    ).offset(skip).limit(limit).all()

# Función para obtener equipo por ID
def get_equipo_by_id(db: Session, equipo_id: int):
    return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
        models.Equipo.id == equipo_id
    ).first()

# Función para actualizar equipo
def update_equipo(db: Session, equipo_id: int, equipo: EquipoUpdate):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        update_data = equipo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_equipo, key, value)
        db.commit()
        db.refresh(db_equipo)
    return db_equipo

# Función para eliminación lógica de equipo
def soft_delete_equipo(db: Session, equipo_id: int):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        db_equipo.eliminado_logico = True
        db.commit()
        db.refresh(db_equipo)
    return db_equipo

# Función para buscar equipos por varios criterios
def search_equipos(db: Session, nombre: str = None, grupo: str = None, pais: str = None, eliminado: bool = False):
    query = db.query(models.Equipo).filter(models.Equipo.eliminado_logico == eliminado)
    if nombre:
        query = query.filter(models.Equipo.nombre.ilike(f"%{nombre}%"))
    if grupo:
        query = query.filter(models.Equipo.grupo.ilike(f"%{grupo}%"))
    if pais:
        query = query.filter(models.Equipo.pais.ilike(f"%{pais}%"))

    return query.all()

# --- NUEVAS FUNCIONES PARA ESTADÍSTICAS ---

# Función para obtener equipos ordenados por el total de goles de sus jugadores
def get_teams_by_total_goals(db: Session, limit: int = 10):
    return db.query(
        models.Equipo,
        func.sum(models.Jugador.goles).label("total_goles")
    ).join(models.Jugador).filter(
        models.Equipo.eliminado_logico == False,
        models.Jugador.eliminado_logico == False
    ).group_by(models.Equipo.id).order_by(func.sum(models.Jugador.goles).desc()).limit(limit).all()

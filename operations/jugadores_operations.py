# operations/jugadores_operations.py
from sqlalchemy.orm import Session, joinedload
from data import models
from data.models import JugadorCreate, JugadorUpdate
from typing import Optional

# Función para crear un nuevo jugador en la base de datos
def create_jugador(db: Session, jugador: JugadorCreate):
    db_jugador = models.Jugador(
        nombre=jugador.nombre,
        equipo_id=jugador.equipo_id,
        posicion=jugador.posicion,
        edad=jugador.edad,
        nacionalidad=jugador.nacionalidad,
        goles=jugador.goles,
        asistencias=jugador.asistencias,
    )
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def get_all_jugadores(db: Session, skip: int = 0, limit: Optional[int] = None):
    query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == False
    ).offset(skip)

    if limit is not None:
        query = query.limit(limit)

    return query.all()


# Función para obtener un jugador por su ID
def get_jugador_by_id(db: Session, jugador_id: int):
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.id == jugador_id
    ).first()

# Función para actualizar un jugador existente
def update_jugador(db: Session, jugador_id: int, jugador: JugadorUpdate):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        update_data = jugador.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_jugador, key, value)
        db.commit()
        db.refresh(db_jugador)
    return db_jugador

# Función para realizar una eliminación lógica de un jugador
def soft_delete_jugador(db: Session, jugador_id: int):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        db_jugador.eliminado_logico = True
        db.commit()
        db.refresh(db_jugador)
    return db_jugador

# Función para buscar jugadores por varios criterios (ACTUALIZADA)
def search_jugadores(
    db: Session,
    nombre: Optional[str] = None, # Este es el 'query' general de FastAPI
    equipo_id: Optional[int] = None,
    posicion: Optional[str] = None,
    nacionalidad: Optional[str] = None,
    id: Optional[int] = None,
    eliminado: bool = False
):
    query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(models.Jugador.eliminado_logico == eliminado)

    # Filtros iniciales se guardan en una lista
    filters = []

    if nombre:
        # Si se proporciona un nombre (el 'query' general),
        # busca en el nombre del jugador O en el nombre del equipo asociado
        filters.append(
            or_(
                models.Jugador.nombre.ilike(f"%{nombre}%"),
                models.Jugador.equipo_obj.has(models.Equipo.nombre.ilike(f"%{nombre}%"))
            )
        )
    if equipo_id:
        filters.append(models.Jugador.equipo_id == equipo_id)
    if posicion:
        filters.append(models.Jugador.posicion.ilike(f"%{posicion}%"))
    if nacionalidad:
        filters.append(models.Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))
    if id:
        filters.append(models.Jugador.id == id)

    # Aplica todos los filtros
    if filters:
        query = query.filter(*filters)

    return query.all()

# --- FUNCIONES PARA ESTADÍSTICAS ---

# Función para obtener los máximos goleadores
def get_top_scorers(db: Session, limit: int = 10):
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == False
    ).order_by(models.Jugador.goles.desc()).limit(limit).all()

# Función para obtener los máximos asistentes
def get_top_assisters(db: Session, limit: int = 10):
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == False
    ).order_by(models.Jugador.asistencias.desc()).limit(limit).all()

# --- NUEVA FUNCIÓN: Obtener jugadores eliminados lógicamente ---
def get_soft_deleted_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == True
    ).offset(skip).limit(limit).all()
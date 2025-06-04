# operations/jugadores_operations.py
from sqlalchemy.orm import Session, joinedload
from data import models
from data.models import JugadorCreate, JugadorUpdate

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
        # imagen_url ya no es parte del modelo Jugador
    )
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

# Función para obtener todos los jugadores (filtrando los eliminados lógicamente)
def get_all_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == False
    ).offset(skip).limit(limit).all()

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
        # Asegurarse de que imagen_url no se intente actualizar si no existe en el modelo
        if 'imagen_url' in update_data: # Esto es una precaución, ya no debería estar en JugadorUpdate
            del update_data['imagen_url']
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

# Función para buscar jugadores por varios criterios
def search_jugadores(db: Session, nombre: str = None, equipo_id: int = None, posicion: str = None, nacionalidad: str = None, eliminado: bool = False):
    query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(models.Jugador.eliminado_logico == eliminado)
    if nombre:
        query = query.filter(models.Jugador.nombre.ilike(f"%{nombre}%"))
    if equipo_id:
        query = query.filter(models.Jugador.equipo_id == equipo_id)
    if posicion:
        query = query.filter(models.Jugador.posicion.ilike(f"%{posicion}%"))
    if nacionalidad:
        query = query.filter(models.Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))

    return query.all()

# --- FUNCIONES PARA ESTADÍSTICAS (se mantienen, pero sin imagen_url) ---

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

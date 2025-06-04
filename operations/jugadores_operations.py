# operations/jugadores_operations.py
from sqlalchemy.orm import Session, joinedload # Importa joinedload para cargar relaciones
from data import models # Importa tus modelos de SQLAlchemy
from data.models import JugadorCreate, JugadorUpdate # Importa los esquemas de Pydantic

# Función para crear un nuevo jugador en la base de datos
def create_jugador(db: Session, jugador: JugadorCreate):
    # Crea una instancia del modelo Jugador con los datos proporcionados
    db_jugador = models.Jugador(
        nombre=jugador.nombre,
        equipo_id=jugador.equipo_id,
        posicion=jugador.posicion,
        edad=jugador.edad,
        nacionalidad=jugador.nacionalidad,
        goles=jugador.goles,
        asistencias=jugador.asistencias,
        imagen_url=jugador.imagen_url
    )
    db.add(db_jugador) # Añade el nuevo jugador a la sesión
    db.commit() # Guarda los cambios en la base de datos
    db.refresh(db_jugador) # Refresca el objeto para obtener su ID y otros campos generados
    return db_jugador

# Función para obtener todos los jugadores (filtrando los eliminados lógicamente)
def get_all_jugadores(db: Session, skip: int = 0, limit: int = 100):
    # Carga los objetos de Equipo relacionados usando joinedload para evitar N+1 queries
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.eliminado_logico == False # Filtra solo los jugadores no eliminados lógicamente
    ).offset(skip).limit(limit).all()

# Función para obtener un jugador por su ID
def get_jugador_by_id(db: Session, jugador_id: int):
    # Carga el objeto de Equipo relacionado
    return db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(
        models.Jugador.id == jugador_id
    ).first()

# Función para actualizar un jugador existente
def update_jugador(db: Session, jugador_id: int, jugador: JugadorUpdate):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        # Convierte el Pydantic model a un diccionario, excluyendo campos no establecidos
        update_data = jugador.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_jugador, key, value) # Actualiza los atributos del modelo de DB
        db.commit()
        db.refresh(db_jugador)
    return db_jugador

# Función para realizar una eliminación lógica de un jugador
def soft_delete_jugador(db: Session, jugador_id: int):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        db_jugador.eliminado_logico = True # Marca el jugador como eliminado lógicamente
        db.commit()
        db.refresh(db_jugador)
    return db_jugador

# Función para buscar jugadores por varios criterios
def search_jugadores(db: Session, nombre: str = None, equipo_id: int = None, posicion: str = None, nacionalidad: str = None, eliminado: bool = False):
    # Construye la consulta base, filtrando por el estado de eliminación lógica
    query = db.query(models.Jugador).options(joinedload(models.Jugador.equipo_obj)).filter(models.Jugador.eliminado_logico == eliminado)
    if nombre:
        query = query.filter(models.Jugador.nombre.ilike(f"%{nombre}%")) # Búsqueda insensible a mayúsculas/minúsculas
    if equipo_id:
        query = query.filter(models.Jugador.equipo_id == equipo_id)
    if posicion:
        query = query.filter(models.Jugador.posicion.ilike(f"%{posicion}%"))
    if nacionalidad:
        query = query.filter(models.Jugador.nacionalidad.ilike(f"%{nacionalidad}%"))

    return query.all()

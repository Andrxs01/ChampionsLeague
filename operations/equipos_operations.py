# operations/equipos_operations.py
from sqlalchemy.orm import Session, joinedload # Importa joinedload para cargar relaciones
from data import models # Importa tus modelos de SQLAlchemy
from data.models import EquipoCreate, EquipoUpdate # Importa los esquemas de Pydantic

# Función para crear un nuevo equipo en la base de datos
def create_equipo(db: Session, equipo: EquipoCreate):
    # Crea una instancia del modelo Equipo con los datos proporcionados
    db_equipo = models.Equipo(
        nombre=equipo.nombre,
        pais=equipo.pais,
        grupo=equipo.grupo,
        imagen_url=equipo.imagen_url
    )
    db.add(db_equipo) # Añade el nuevo equipo a la sesión
    db.commit() # Guarda los cambios en la base de datos
    db.refresh(db_equipo) # Refresca el objeto para obtener su ID
    return db_equipo

# Función para obtener todos los equipos (filtrando los eliminados lógicamente)
def get_all_equipos(db: Session, skip: int = 0, limit: int = 100):
    # Carga los objetos de Jugador relacionados usando joinedload
    return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
        models.Equipo.eliminado_logico == False # Filtra solo los equipos no eliminados lógicamente
    ).offset(skip).limit(limit).all()

# Función para obtener un equipo por su ID
def get_equipo_by_id(db: Session, equipo_id: int):
    # Carga los objetos de Jugador relacionados
    return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
        models.Equipo.id == equipo_id
    ).first()

# Función para actualizar un equipo existente
def update_equipo(db: Session, equipo_id: int, equipo: EquipoUpdate):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        # Convierte el Pydantic model a un diccionario, excluyendo campos no establecidos
        update_data = equipo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_equipo, key, value) # Actualiza los atributos del modelo de DB
        db.commit()
        db.refresh(db_equipo)
    return db_equipo

# Función para realizar una eliminación lógica de un equipo
def soft_delete_equipo(db: Session, equipo_id: int):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        db_equipo.eliminado_logico = True # Marca el equipo como eliminado lógicamente
        db.commit()
        db.refresh(db_equipo)
    return db_equipo

# Función para buscar equipos por varios criterios
def search_equipos(db: Session, nombre: str = None, grupo: str = None, pais: str = None, eliminado: bool = False):
    # Construye la consulta base, filtrando por el estado de eliminación lógica
    query = db.query(models.Equipo).filter(models.Equipo.eliminado_logico == eliminado)
    if nombre:
        query = query.filter(models.Equipo.nombre.ilike(f"%{nombre}%")) # Búsqueda insensible a mayúsculas/minúsculas
    if grupo:
        query = query.filter(models.Equipo.grupo.ilike(f"%{grupo}%"))
    if pais:
        query = query.filter(models.Equipo.pais.ilike(f"%{pais}%"))

    return query.all()

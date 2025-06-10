# operations/equipos_operations.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, OperationalError
from data import models
from data.models import EquipoCreate, EquipoUpdate
from typing import Optional

# --- Operaciones CRUD para Equipos ---

def create_equipo(db: Session, equipo: EquipoCreate):
    """
    Crea un nuevo equipo en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        equipo (EquipoCreate): Los datos del equipo a crear.

    Returns:
        models.Equipo: El equipo recién creado.

    Raises:
        IntegrityError: Si hay un problema de integridad de datos (ej. nombre duplicado).
        Exception: Para otros errores inesperados durante la creación.
    """
    try:
        # Asegúrate de convertir el objeto HttpUrl a str antes de pasarlo al modelo ORM.
        # Si equipo.imagen_url es None, se pasará None, lo cual es manejado por nullable=True en el modelo.
        imagen_url_str = str(equipo.imagen_url) if equipo.imagen_url else None

        db_equipo = models.Equipo(
            nombre=equipo.nombre,
            pais=equipo.pais,
            grupo=equipo.grupo,
            imagen_url=imagen_url_str
        )
        db.add(db_equipo)
        db.commit()
        db.refresh(db_equipo)
        return db_equipo
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al crear el equipo! Detalles: {e}")
        raise ValueError("Ya existe un equipo con ese nombre o datos inválidos.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al crear el equipo: {e}")
        raise

def get_all_equipos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los equipos no eliminados lógicamente.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[models.Equipo]: Una lista de equipos.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
            models.Equipo.eliminado_logico == False
        ).offset(skip).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener equipos! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al obtener todos los equipos! Detalles: {e}")
        raise

def get_equipo_by_id(db: Session, equipo_id: int):
    """
    Obtiene un equipo por su ID.

    Args:
        db (Session): La sesión de la base de datos.
        equipo_id (int): El ID del equipo.

    Returns:
        Optional[models.Equipo]: El equipo encontrado o None si no existe.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Equipo).options(joinedload(models.Equipo.jugadores)).filter(
            models.Equipo.id == equipo_id
        ).first()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar equipo por ID! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos.")
    except Exception as e:
        print(f"¡Error desconocido al buscar equipo por ID {equipo_id}! Detalles: {e}")
        raise

def update_equipo(db: Session, equipo_id: int, equipo: EquipoUpdate):
    """
    Actualiza los datos de un equipo existente.

    Args:
        db (Session): La sesión de la base de datos.
        equipo_id (int): El ID del equipo a actualizar.
        equipo (EquipoUpdate): Los nuevos datos para el equipo.

    Returns:
        Optional[models.Equipo]: El equipo actualizado o None si no se encontró.

    Raises:
        IntegrityError: Si la actualización causa un problema de integridad de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
        if db_equipo:
            update_data = equipo.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                # Convertir HttpUrl a str si es necesario
                if key == "imagen_url" and value is not None:
                    setattr(db_equipo, key, str(value))
                else:
                    setattr(db_equipo, key, value)
            db.commit()
            db.refresh(db_equipo)
        return db_equipo
    except IntegrityError as e:
        db.rollback()
        print(f"¡Error de integridad al actualizar el equipo! Detalles: {e}")
        raise ValueError("No se pudo actualizar el equipo debido a datos inválidos o duplicados.")
    except Exception as e:
        db.rollback()
        print(f"¡Oops! Un error inesperado ocurrió al actualizar el equipo con ID {equipo_id}: {e}")
        raise

def soft_delete_equipo(db: Session, equipo_id: int):
    """
    Realiza una eliminación lógica de un equipo (lo marca como eliminado).

    Args:
        db (Session): La sesión de la base de datos.
        equipo_id (int): El ID del equipo a eliminar lógicamente.

    Returns:
        Optional[models.Equipo]: El equipo marcado como eliminado o None si no se encontró.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
        if db_equipo:
            db_equipo.eliminado_logico = True
            db.commit()
            db.refresh(db_equipo)
        return db_equipo
    except OperationalError as e:
        db.rollback()
        print(f"¡Problema de conexión con la base de datos al eliminar equipo {equipo_id}! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para eliminar el equipo.")
    except Exception as e:
        db.rollback()
        print(f"¡Error desconocido al intentar eliminar lógicamente el equipo con ID {equipo_id}! Detalles: {e}")
        raise

def search_equipos(
    db: Session,
    nombre: Optional[str] = None,
    grupo: Optional[str] = None,
    pais: Optional[str] = None,
    id_equipo: Optional[int] = None, # Renombrado para mayor claridad
    eliminado: bool = False
):
    """
    Busca equipos por varios criterios.

    Args:
        db (Session): La sesión de la base de datos.
        nombre (Optional[str]): Nombre parcial del equipo.
        grupo (Optional[str]): Grupo del equipo.
        pais (Optional[str]): País del equipo.
        id_equipo (Optional[int]): ID exacto del equipo.
        eliminado (bool): Si se deben incluir equipos eliminados lógicamente.

    Returns:
        List[models.Equipo]: Una lista de equipos que coinciden con los criterios.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        query = db.query(models.Equipo).filter(models.Equipo.eliminado_logico == eliminado)
        if nombre:
            # Buscar por nombre (case-insensitive)
            query = query.filter(models.Equipo.nombre.ilike(f"%{nombre}%"))
        if grupo:
            # Buscar por grupo (case-insensitive)
            query = query.filter(models.Equipo.grupo.ilike(f"%{grupo}%"))
        if pais:
            # Buscar por país (case-insensitive)
            query = query.filter(models.Equipo.pais.ilike(f"%{pais}%"))
        if id_equipo:
            # Buscar por ID exacto
            query = query.filter(models.Equipo.id == id_equipo)

        return query.all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al buscar equipos! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para realizar la búsqueda.")
    except Exception as e:
        print(f"¡Error desconocido al buscar equipos! Detalles: {e}")
        raise

# --- Funciones para Estadísticas y reportes ---

def get_teams_by_total_goals(db: Session, limit: int = 10):
    """
    Obtiene los equipos ordenados por el total de goles de sus jugadores activos.

    Args:
        db (Session): La sesión de la base de datos.
        limit (int): El número máximo de equipos a devolver.

    Returns:
        List[Tuple[models.Equipo, int]]: Una lista de tuplas con el equipo y su total de goles.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(
            models.Equipo,
            func.sum(models.Jugador.goles).label("total_goles")
        ).join(models.Jugador).filter(
            models.Equipo.eliminado_logico == False,
            models.Jugador.eliminado_logico == False
        ).group_by(models.Equipo.id).order_by(func.sum(models.Jugador.goles).desc()).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener equipos por goles! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener estadísticas de goles.")
    except Exception as e:
        print(f"¡Error desconocido al obtener equipos por total de goles! Detalles: {e}")
        raise

def get_soft_deleted_equipos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todos los equipos que han sido eliminados lógicamente.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): Número de registros a omitir.
        limit (int): Número máximo de registros a devolver.

    Returns:
        List[models.Equipo]: Una lista de equipos eliminados lógicamente.

    Raises:
        OperationalError: Si hay un problema de conexión con la base de datos.
        Exception: Para otros errores inesperados.
    """
    try:
        return db.query(models.Equipo).filter(
            models.Equipo.eliminado_logico == True
        ).offset(skip).limit(limit).all()
    except OperationalError as e:
        print(f"¡Problema de conexión con la base de datos al obtener equipos eliminados! Detalles: {e}")
        raise ConnectionError("No se pudo conectar a la base de datos para obtener equipos eliminados.")
    except Exception as e:
        print(f"¡Error desconocido al obtener equipos eliminados lógicamente! Detalles: {e}")
        raise